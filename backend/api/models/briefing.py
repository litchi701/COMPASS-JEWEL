from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BriefingResponse(BaseModel):
    id: int
    market_region: str
    briefing_date: datetime
    content: dict
    created_at: datetime

    class Config:
        from_attributes = True
