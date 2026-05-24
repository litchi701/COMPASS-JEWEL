from types import SimpleNamespace
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import ChatHistory
from api.models.chat import ChatQueryRequest, ChatQueryResponse
from services.agent_service import AgentService
from services.database_query_service import DatabaseQueryService
from services.hecksong_data_service import HecksongDataService
from services.trace_service import TraceService

router = APIRouter()
agent_service = AgentService()


def _article_to_record(article: dict, index: int):
    """将 hecksong 条目转为 trace/agent 可用的记录对象"""
    return SimpleNamespace(
        id=index + 1,
        url=article.get("url", ""),
        source_platform=article.get("source_platform", "News"),
        content=f"{article.get('title', '')}\n{article.get('content', '')}",
        market_region=article.get("market_region", "JP"),
        crawl_time=datetime.now(),  # 使用当前时间作为默认值
        keywords=article.get("keywords", ""),
    )


@router.post("/query", response_model=ChatQueryResponse)
def query_agent(request: ChatQueryRequest, db: Session = Depends(get_db)):
    """
    发送用户提问给 Agent 3
    """
    market = (request.market or "JP").upper()
    related_records = []

    try:
        related_records = DatabaseQueryService.search_by_keywords(
            db=db,
            keywords=[request.question],
            market_region=market,
        )
    except Exception:
        related_records = []

    if not related_records:
        hk_articles = HecksongDataService.search_for_agent(
            request.question, market, limit=10
        )
        related_records = [
            _article_to_record(a, i) for i, a in enumerate(hk_articles)
        ]

    try:
        agent_response = agent_service.call_query_agent(
            question=request.question,
            context_data=related_records,
        )

        trace_report = TraceService.generate_trace_report(
            answer=agent_response.get("answer", ""),
            source_records=related_records,
        )

        try:
            chat_record = ChatHistory(
                user_question=request.question,
                agent_response=trace_report["answer"],
                related_record_ids=[
                    r.id for r in related_records if getattr(r, "id", None)
                ],
            )
            db.add(chat_record)
            db.commit()
        except Exception:
            db.rollback()

        return ChatQueryResponse(
            answer=trace_report["answer"],
            related_records=trace_report["sources"],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")


@router.get("/history")
def get_chat_history(limit: int = 50, db: Session = Depends(get_db)):
    """
    获取对话历史
    """
    history = (
        db.query(ChatHistory)
        .order_by(ChatHistory.created_at.desc())
        .limit(limit)
        .all()
    )

    return history


@router.delete("/history/{id}")
def delete_chat_message(id: int, db: Session = Depends(get_db)):
    """
    删除指定对话记录
    """
    chat = db.query(ChatHistory).filter(ChatHistory.id == id).first()

    if not chat:
        raise HTTPException(status_code=404, detail="对话记录不存在")

    db.delete(chat)
    db.commit()

    return {"message": f"已删除对话记录 {id}"}


@router.delete("/history/all")
def clear_chat_history(db: Session = Depends(get_db)):
    """
    清空所有对话历史
    """
    deleted_count = db.query(ChatHistory).delete()
    db.commit()

    return {"message": f"已清空所有对话历史，共删除 {deleted_count} 条记录"}
