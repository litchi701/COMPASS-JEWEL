"""
溯源服务
负责生成可追溯的报告
"""

from typing import List, Dict
from database.models import CrawlRecord

class TraceService:
    """
    溯源服务
    为 Agent 3 的回答提供数据来源追溯
    """

    @staticmethod
    def generate_trace_report(
        answer: str,
        source_records: List[CrawlRecord]
    ) -> Dict:
        """
        生成溯源报告

        Args:
            answer: Agent 的回答
            source_records: 相关的爬虫记录

        Returns:
            Dict: 包含回答和溯源信息的报告
        """
        # 格式化源记录
        formatted_sources = [
            TraceService.format_source_record(record)
            for record in source_records
        ]

        return {
            'answer': answer,
            'sources': formatted_sources,
            'source_count': len(formatted_sources)
        }

    @staticmethod
    def format_source_record(record: CrawlRecord) -> Dict:
        """
        格式化单条爬虫记录为溯源信息

        Args:
            record: 爬虫记录

        Returns:
            Dict: 格式化后的溯源信息
        """
        return {
            'id': record.id,
            'url': record.url,
            'source_platform': record.source_platform or '未知平台',
            'content': record.content or '',
            'market_region': record.market_region,
            'crawl_time': record.crawl_time.isoformat() if record.crawl_time else None,
            'keywords': record.keywords
        }

    @staticmethod
    def build_trace_summary(source_records: List[CrawlRecord]) -> str:
        """
        构建溯源摘要文本

        Args:
            source_records: 爬虫记录列表

        Returns:
            str: 溯源摘要文本
        """
        if not source_records:
            return "未找到相关数据来源。"

        summary_parts = [f"根据以下 {len(source_records)} 条爬虫记录分析：\n"]

        for idx, record in enumerate(source_records, 1):
            crawl_time = record.crawl_time.strftime('%Y-%m-%d %H:%M') if record.crawl_time else '未知时间'
            platform = record.source_platform or '未知平台'

            summary_parts.append(
                f"{idx}. [{crawl_time}] 来源：{platform}\n"
                f"   URL: {record.url}\n"
                f"   内容摘要：{record.content[:100] if record.content else '无内容'}...\n"
            )

        return "\n".join(summary_parts)

