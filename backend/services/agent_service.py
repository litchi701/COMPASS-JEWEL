"""
Agent 服务模块
通过 OpenAI 兼容接口调用 FindCG / Claude
"""

import json
import logging
from typing import Any, List, Optional, Union

from openai import OpenAI

from config.settings import AGENT_API_KEY, AGENT_BASE_URL, AGENT_MODEL

logger = logging.getLogger(__name__)

SYSTEM_PROMPT_QUERY = """你是 COMPASS JEWEL 的战略情报分析助手（Agent 3）。
根据用户问题和提供的爬虫记录上下文，给出简洁、可执行的市场洞察。
若上下文为空，基于珠宝行业常识回答，并说明当前无数据库溯源记录。
回答使用中文，条理清晰，避免空泛套话。"""

SYSTEM_PROMPT_SUMMARY = """你是 COMPASS JEWEL 的分析助手（Agent 2）。
根据爬虫记录生成每日战略简报要点，输出 JSON 对象，仅包含以下键（英文键名）：
- keyMarketShift: 关键市场变化（字符串）
- socialTrend: 社交/消费趋势（字符串）
- competitorMove: 竞品或行业动态（字符串，可选）
- recommendation: 简要建议（字符串，可选）
不要输出 markdown 代码块，只输出合法 JSON。"""


def _normalize_base_url(url: str) -> str:
    base = (url or "").strip().rstrip("/")
    if not base:
        return "https://www.findcg.com/v1"
    if not base.endswith("/v1"):
        base = f"{base}/v1"
    return base


def _format_context_records(records: List[Any]) -> str:
    if not records:
        return "（暂无相关爬虫记录）"

    parts = []
    for idx, record in enumerate(records[:15], 1):
        if isinstance(record, dict):
            platform = record.get("source_platform") or "未知"
            url = record.get("url") or ""
            content = (record.get("content") or "")[:500]
            market = record.get("market_region") or ""
        else:
            platform = getattr(record, "source_platform", None) or "未知"
            url = getattr(record, "url", "") or ""
            content = (getattr(record, "content", None) or "")[:500]
            market = getattr(record, "market_region", None) or ""

        parts.append(
            f"[{idx}] 市场:{market} | 平台:{platform}\n"
            f"URL: {url}\n"
            f"内容: {content}\n"
        )
    return "\n".join(parts)


class AgentService:
    """Agent 2 / Agent 3 调用服务（OpenAI 兼容 API）"""

    def __init__(self):
        self.api_key = AGENT_API_KEY
        self.model = AGENT_MODEL or "claude-sonnet-4-6"
        self.base_url = _normalize_base_url(AGENT_BASE_URL)
        self._client: Optional[OpenAI] = None

    def _get_client(self) -> OpenAI:
        if not self.api_key:
            raise ValueError("未配置 AGENT_API_KEY，请在 backend/.env 中设置")
        if self._client is None:
            self._client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
            )
        return self._client

    def _chat(
        self,
        system: str,
        user: str,
        *,
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> str:
        client = self._get_client()
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        message = response.choices[0].message
        return (message.content or "").strip()

    def call_query_agent(
        self, question: str, context_data: List[Any]
    ) -> dict:
        """
        调用 Agent 3：回答用户提问

        Returns:
            dict: {"answer": str}
        """
        context_text = _format_context_records(context_data)
        user_prompt = (
            f"用户问题：{question}\n\n"
            f"相关爬虫记录（共 {len(context_data)} 条）：\n{context_text}"
        )

        try:
            answer = self._chat(SYSTEM_PROMPT_QUERY, user_prompt)
            return {"answer": answer}
        except Exception as e:
            logger.exception("Agent 3 调用失败")
            return {
                "answer": (
                    f"暂时无法连接分析服务（{type(e).__name__}）。"
                    "请检查 API 密钥、网络或 base_url 配置。"
                )
            }

    def call_summary_agent(self, crawl_data: List[Any]) -> dict:
        """
        调用 Agent 2：总结分析爬取的数据

        Returns:
            dict: 简报 JSON 字段
        """
        context_text = _format_context_records(crawl_data)
        user_prompt = f"请根据以下爬虫记录生成战略简报 JSON：\n\n{context_text}"

        raw = ""
        try:
            raw = self._chat(
                SYSTEM_PROMPT_SUMMARY,
                user_prompt,
                max_tokens=1024,
                temperature=0.5,
            )
            # 去掉可能的 ```json 包裹
            text = raw.strip()
            if text.startswith("```"):
                lines = text.split("\n")
                text = "\n".join(
                    lines[1:-1] if lines[-1].strip() == "```" else lines[1:]
                )
            parsed = json.loads(text)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            logger.warning("Agent 2 返回非 JSON，使用原文")
            return {
                "keyMarketShift": raw[:500] if raw else "分析完成",
                "socialTrend": f"参考 {len(crawl_data)} 条记录",
            }
        except Exception as e:
            logger.exception("Agent 2 调用失败")
            return {
                "keyMarketShift": f"分析服务暂不可用：{type(e).__name__}",
                "socialTrend": f"共 {len(crawl_data)} 条爬虫记录待分析",
            }

        return {
            "keyMarketShift": "分析完成",
            "socialTrend": f"共 {len(crawl_data)} 条记录",
        }
