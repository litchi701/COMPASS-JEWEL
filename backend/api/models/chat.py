from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatQueryRequest(BaseModel):
    question: str

class SourceRecord(BaseModel):
    id: int
    url: str
    source_platform: str
    content: str
    crawl_time: datetime

class ChatQueryResponse(BaseModel):
    answer: str
    related_records: List[SourceRecord]

class ChatHistoryItem(BaseModel):
    id: int
    user_question: str
    agent_response: str
    related_record_ids: Optional[List[int]]
    created_at: datetime

    class Config:
        from_attributes = True
