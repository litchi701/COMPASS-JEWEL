from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import ChatHistory
from api.models.chat import ChatQueryRequest, ChatQueryResponse, ChatHistoryItem
from services.agent_service import AgentService
from services.database_query_service import DatabaseQueryService
from services.trace_service import TraceService

router = APIRouter()
agent_service = AgentService()

@router.post("/query", response_model=ChatQueryResponse)
def query_agent(request: ChatQueryRequest, db: Session = Depends(get_db)):
    """
    发送用户提问给 Agent 3
    """
    try:
        # 1. 从数据库查询相关记录
        related_records = DatabaseQueryService.search_by_keywords(
            db=db,
            keywords=[request.question]
        )

        # 2. 调用 Agent 3 生成回答（预留）
        agent_response = agent_service.call_query_agent(
            question=request.question,
            context_data=related_records
        )

        # 3. 生成溯源报告
        trace_report = TraceService.generate_trace_report(
            answer=agent_response.get('answer', ''),
            source_records=related_records
        )

        # 4. 保存对话历史
        chat_record = ChatHistory(
            user_question=request.question,
            agent_response=trace_report['answer'],
            related_record_ids=[r.id for r in related_records]
        )
        db.add(chat_record)
        db.commit()

        return ChatQueryResponse(
            answer=trace_report['answer'],
            related_records=trace_report['sources']
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")

@router.get("/history")
def get_chat_history(limit: int = 50, db: Session = Depends(get_db)):
    """
    获取对话历史
    """
    history = db.query(ChatHistory).order_by(
        ChatHistory.created_at.desc()
    ).limit(limit).all()

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
