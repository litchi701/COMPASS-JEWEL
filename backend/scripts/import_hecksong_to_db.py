#!/usr/bin/env python3
"""
将 data-in-hecksong 数据导入 MySQL crawl_records 表
需先配置 .env 中的 DATABASE_URL，并执行 init_db.sql
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from email.utils import parsedate_to_datetime

from database.connection import SessionLocal
from database.models import CrawlRecord
from services.hecksong_data_service import HecksongDataService

MARKETS = ["JP", "KR", "SEA", "US"]


def main():
    db = SessionLocal()
    inserted = 0
    try:
        for market in MARKETS:
            for row in HecksongDataService.to_crawl_records(market):
                crawl_time = datetime.utcnow()
                if row.get("crawl_time"):
                    try:
                        raw = row["crawl_time"]
                        if "T" in str(raw):
                            crawl_time = datetime.fromisoformat(
                                str(raw).replace("Z", "+00:00")
                            )
                        else:
                            crawl_time = parsedate_to_datetime(raw)
                    except (TypeError, ValueError, OverflowError):
                        pass

                exists = (
                    db.query(CrawlRecord)
                    .filter(CrawlRecord.url == row["url"])
                    .first()
                )
                if exists:
                    continue

                db.add(
                    CrawlRecord(
                        url=row["url"][:500],
                        source_platform=row["source_platform"],
                        content=row["content"],
                        market_region=row["market_region"],
                        keywords=row["keywords"],
                        crawl_time=crawl_time,
                    )
                )
                inserted += 1

        db.commit()
        print(f"导入完成，新增 {inserted} 条 crawl_records")
    finally:
        db.close()


if __name__ == "__main__":
    main()
