from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime
from database.connection import Base

# 爬虫记录表
class CrawlRecord(Base):
    __tablename__ = "crawl_records"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), nullable=False)
    source_platform = Column(String(50))
    content = Column(Text)
    market_region = Column(String(20))
    keywords = Column(String(200))
    crawl_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# 简报表
class Briefing(Base):
    __tablename__ = "briefings"

    id = Column(Integer, primary_key=True, index=True)
    market_region = Column(String(20))
    briefing_date = Column(DateTime, nullable=False)
    content = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

# 对话历史表
class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_question = Column(Text, nullable=False)
    agent_response = Column(Text, nullable=False)
    related_record_ids = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
