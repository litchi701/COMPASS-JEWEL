"""
Hecksong 黑客松数据集服务
数据源: https://github.com/Lby1102/data-in-hecksong
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import quote

import httpx

from config.settings import HECKSONG_DATA_PATH, HECKSONG_DATA_URL

# 数据仓库 region -> 前端市场代码
REGION_TO_MARKET = {
    "Japan": "JP",
    "Korea": "KR",
    "Southeast_Asia": "SEA",
    "Global": "GLOBAL",
}

MARKET_TO_REGIONS: Dict[str, List[str]] = {
    "JP": ["Japan", "Global"],
    "KR": ["Korea", "Global"],
    "SEA": ["Southeast_Asia", "Global"],
    "US": ["Global"],
    "GLOBAL": ["Global"],
}

JEWELRY_KEYWORDS = re.compile(
    r"jewel|jewelry|jewellery|gold|silver|platinum|gem|diamond|pearl|"
    r"ring|necklace|bracelet|earring|watch|luxury|联名|珠宝|金饰|首饰",
    re.IGNORECASE,
)

US_KEYWORDS = re.compile(
    r"\b(US|U\.S\.|USA|America|American|United States)\b",
    re.IGNORECASE,
)


class HecksongDataService:
    _articles: Optional[List[Dict[str, Any]]] = None

    @classmethod
    def _data_file(cls) -> Path:
        return Path(HECKSONG_DATA_PATH)

    @classmethod
    def refresh_from_remote(cls) -> int:
        """从 GitHub 拉取最新 ALL_ARTICLES.json"""
        path = cls._data_file()
        path.parent.mkdir(parents=True, exist_ok=True)
        with httpx.Client(timeout=60.0) as client:
            resp = client.get(HECKSONG_DATA_URL)
            resp.raise_for_status()
            path.write_bytes(resp.content)
        cls._articles = None
        return len(cls.load_articles())

    @classmethod
    def load_articles(cls) -> List[Dict[str, Any]]:
        if cls._articles is not None:
            return cls._articles

        path = cls._data_file()
        if not path.is_file():
            cls.refresh_from_remote()

        raw = json.loads(path.read_text(encoding="utf-8"))
        cls._articles = raw if isinstance(raw, list) else []
        return cls._articles

    @staticmethod
    def _parse_date(pub_date: str) -> Optional[datetime]:
        if not pub_date:
            return None
        try:
            dt = parsedate_to_datetime(pub_date)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except (TypeError, ValueError, OverflowError):
            return None

    @staticmethod
    def _article_url(article: Dict[str, Any], index: int) -> str:
        link = article.get("link") or article.get("url")
        if link:
            return str(link)[:500]
        title = article.get("title") or "article"
        region = article.get("region") or "unknown"
        return f"https://news.google.com/search?q={quote(title)}&region={region}&i={index}"

    @classmethod
    def _normalize(cls, article: Dict[str, Any], index: int) -> Dict[str, Any]:
        region = article.get("region") or "Global"
        market = REGION_TO_MARKET.get(region, "GLOBAL")
        title = (article.get("title") or "").strip()
        snippet = (article.get("snippet") or title).strip()
        source = (article.get("source") or "Unknown").strip()
        pub_dt = cls._parse_date(article.get("pubDate") or "")

        text_blob = f"{title} {snippet}"
        passed_gate = bool(JEWELRY_KEYWORDS.search(text_blob))

        return {
            "id": f"{region}-{index}",
            "market_region": market,
            "data_region": region,
            "title": title,
            "content": snippet,
            "source_platform": source,
            "url": cls._article_url(article, index),
            "pub_date": pub_dt.isoformat() if pub_dt else None,
            "passed_gate": passed_gate,
            "keywords": cls._extract_keywords(title),
        }

    @staticmethod
    def _extract_keywords(title: str) -> str:
        words = re.findall(r"[A-Za-z0-9\u4e00-\u9fff]{3,}", title)
        return ",".join(words[:5])

    @classmethod
    def _filter_for_market(
        cls, articles: List[Dict[str, Any]], market: str
    ) -> List[Dict[str, Any]]:
        market = market.upper()
        regions = MARKET_TO_REGIONS.get(market, ["Global"])
        filtered = [a for a in articles if a.get("region") in regions]

        if market == "US":
            filtered = [
                a
                for a in filtered
                if US_KEYWORDS.search(
                    f"{a.get('title', '')} {a.get('snippet', '')}"
                )
            ]
        return filtered

    @classmethod
    def get_market_articles(cls, market: str) -> List[Dict[str, Any]]:
        all_raw = cls._filter_for_market(cls.load_articles(), market)
        return [cls._normalize(a, i) for i, a in enumerate(all_raw)]

    @classmethod
    def get_feed(cls, market: str, limit: int = 20) -> Dict[str, Any]:
        normalized = cls.get_market_articles(market)
        total_raw = len(normalized)
        passed = [a for a in normalized if a["passed_gate"]]
        total_passed = len(passed)

        # 按发布时间倒序
        passed.sort(
            key=lambda x: x.get("pub_date") or "",
            reverse=True,
        )
        items = passed[:limit]

        filter_rate = (
            round((1 - total_passed / total_raw) * 100, 1) if total_raw else 0.0
        )

        return {
            "market": market.upper(),
            "items": [cls._to_feed_item(a) for a in items],
            "stats": {
                "total_raw": total_raw,
                "total_passed": total_passed,
                "filter_rate": filter_rate,
                "data_source": "Lby1102/data-in-hecksong",
            },
        }

    @staticmethod
    def _to_feed_item(article: Dict[str, Any]) -> Dict[str, Any]:
        pub = article.get("pub_date")
        return {
            "id": article["id"],
            "source": article["source_platform"],
            "time": HecksongDataService._relative_time(pub),
            "content": article["title"] or article["content"],
            "tag": "【双重门控通过】",
            "url": article["url"],
        }

    @staticmethod
    def _relative_time(iso_str: Optional[str]) -> str:
        if not iso_str:
            return "未知时间"
        try:
            dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            delta = now - dt
            hours = int(delta.total_seconds() // 3600)
            if hours < 1:
                return "刚刚"
            if hours < 24:
                return f"{hours}小时前"
            days = hours // 24
            if days < 30:
                return f"{days}天前"
            return dt.strftime("%Y-%m-%d")
        except (TypeError, ValueError):
            return "未知时间"

    @classmethod
    def get_stats(cls, market: Optional[str] = None) -> Dict[str, Any]:
        articles = cls.load_articles()
        if market:
            feed = cls.get_feed(market, limit=9999)
            return feed["stats"]

        by_region: Dict[str, int] = {}
        for a in articles:
            r = a.get("region") or "Unknown"
            by_region[r] = by_region.get(r, 0) + 1

        all_norm = [cls._normalize(a, i) for i, a in enumerate(articles)]
        total = len(all_norm)
        passed = sum(1 for a in all_norm if a["passed_gate"])
        filter_rate = round((1 - passed / total) * 100, 1) if total else 0.0

        return {
            "total_articles": total,
            "total_passed": passed,
            "filter_rate": filter_rate,
            "by_region": by_region,
            "data_source": "Lby1102/data-in-hecksong",
        }

    @classmethod
    def search_for_agent(
        cls, question: str, market: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Agent 3 无数据库时的内存检索"""
        tokens = [t for t in re.split(r"\W+", question) if len(t) >= 2][:8]
        articles = [a for a in cls.get_market_articles(market) if a["passed_gate"]]
        if not tokens:
            return articles[:limit]

        scored: List[tuple] = []
        for a in articles:
            blob = f"{a['title']} {a['content']}".lower()
            score = sum(1 for t in tokens if t.lower() in blob)
            if score > 0:
                scored.append((score, a))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [a for _, a in scored[:limit]] or articles[:limit]

    @classmethod
    def to_crawl_records(cls, market: str) -> List[Dict[str, Any]]:
        """供导入 MySQL 使用"""
        records = []
        for a in cls.get_market_articles(market):
            if not a["passed_gate"]:
                continue
            records.append(
                {
                    "url": a["url"],
                    "source_platform": a["source_platform"],
                    "content": f"{a['title']}\n{a['content']}",
                    "market_region": market.upper(),
                    "keywords": a["keywords"],
                    "crawl_time": a["pub_date"] or datetime.utcnow().isoformat(),
                }
            )
        return records
