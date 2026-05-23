from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import Briefing
from api.models.briefing import BriefingResponse
from datetime import date

router = APIRouter()

@router.get("/{market}", response_model=BriefingResponse)
def get_briefing(market: str, db: Session = Depends(get_db)):
    """
    获取指定市场的最新简报
    """
    # 查询最新的简报
    briefing = db.query(Briefing).filter(
        Briefing.market_region == market.upper()
    ).order_by(Briefing.briefing_date.desc()).first()

    if not briefing:
        raise HTTPException(status_code=404, detail=f"未找到 {market} 市场的简报")

    return briefing

@router.get("/{market}/history")
def get_briefing_history(market: str, limit: int = 10, db: Session = Depends(get_db)):
    """
    获取历史简报
    """
    briefings = db.query(Briefing).filter(
        Briefing.market_region == market.upper()
    ).order_by(Briefing.briefing_date.desc()).limit(limit).all()

    return briefings
