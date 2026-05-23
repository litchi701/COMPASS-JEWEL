"""
数据库查询服务
负责从 SQL 数据库查询爬虫记录
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from database.models import CrawlRecord
from typing import List, Optional
from datetime import datetime

class DatabaseQueryService:
    """
    数据库查询服务
    为 Agent 3 提供数据检索功能
    """

    @staticmethod
    def search_by_keywords(
        db: Session,
        keywords: List[str],
        market_region: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 10
    ) -> List[CrawlRecord]:
        """
        根据关键词搜索爬虫记录

        Args:
            db: 数据库会话
            keywords: 关键词列表
            market_region: 市场区域（可选）
            start_date: 开始时间（可选）
            end_date: 结束时间（可选）
            limit: 返回记录数量限制

        Returns:
            List[CrawlRecord]: 匹配的爬虫记录
        """
        query = db.query(CrawlRecord)

        # 关键词搜索（在 content 或 keywords 字段中）
        if keywords:
            keyword_filters = []
            for keyword in keywords:
                keyword_filters.append(CrawlRecord.content.contains(keyword))
                keyword_filters.append(CrawlRecord.keywords.contains(keyword))
            query = query.filter(or_(*keyword_filters))

        # 市场区域过滤
        if market_region:
            query = query.filter(CrawlRecord.market_region == market_region)

        # 时间范围过滤
        if start_date:
            query = query.filter(CrawlRecord.crawl_time >= start_date)
        if end_date:
            query = query.filter(CrawlRecord.crawl_time <= end_date)

        # 按时间倒序排列，返回最新的记录
        query = query.order_by(CrawlRecord.crawl_time.desc()).limit(limit)

        return query.all()

    @staticmethod
    def get_by_ids(db: Session, record_ids: List[int]) -> List[CrawlRecord]:
        """
        根据 ID 列表获取爬虫记录

        Args:
            db: 数据库会话
            record_ids: 记录 ID 列表

        Returns:
            List[CrawlRecord]: 爬虫记录列表
        """
        return db.query(CrawlRecord).filter(
            CrawlRecord.id.in_(record_ids)
        ).all()

    @staticmethod
    def get_recent_records(
        db: Session,
        market_region: Optional[str] = None,
        limit: int = 20
    ) -> List[CrawlRecord]:
        """
        获取最近的爬虫记录

        Args:
            db: 数据库会话
            market_region: 市场区域（可选）
            limit: 返回记录数量限制

        Returns:
            List[CrawlRecord]: 最近的爬虫记录
        """
        query = db.query(CrawlRecord)

        if market_region:
            query = query.filter(CrawlRecord.market_region == market_region)

        return query.order_by(CrawlRecord.crawl_time.desc()).limit(limit).all()

