from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .auth import get_current_user
from ..database import get_db
from ..models import Conversation, ConversationInsight, Lead, User
from ..services.conversation_service import summarize_transcript

router = APIRouter(prefix="/api/conversations", tags=["Conversations"])
DbSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


class SummarizeRequest(BaseModel):
    lead_id: Optional[int] = None
    title: Optional[str] = "Customer Sync"
    transcript: str


@router.get("")
def list_conversations(
    db: DbSession,
    current_user: CurrentUser,
):
    convs = db.query(Conversation).order_by(Conversation.id.desc()).all()
    results = []
    for c in convs:
        lead = c.lead
        results.append({
            "id": c.id,
            "lead_id": c.lead_id,
            "lead_company": lead.company if lead else "Manufacturing Client",
            "title": c.title,
            "summary": c.summary,
            "sentiment": c.sentiment,
            "sentiment_score": c.sentiment_score,
            "created_at": c.created_at.isoformat() if c.created_at else None,
        })
    return {"conversations": results}


@router.post("/summarize")
def summarize_meeting(
    data: SummarizeRequest,
    db: DbSession,
    current_user: CurrentUser,
):
    if not data.transcript or not data.transcript.strip():
        raise HTTPException(status_code=400, detail="Transcript is required")

    analysis = summarize_transcript(data.transcript)

    conv = Conversation(
        lead_id=data.lead_id,
        title=data.title or f"Meeting on {analysis.get('meeting_date', 'Today')}",
        transcript=data.transcript,
        summary=analysis.get("summary"),
        sentiment=analysis.get("sentiment"),
        sentiment_score=analysis.get("sentiment_score", 0.8),
    )
    db.add(conv)
    db.flush()

    for item in analysis.get("action_items", []):
        ci = ConversationInsight(conversation_id=conv.id, insight_type="action_item", content=item)
        db.add(ci)

    for item in analysis.get("budget_mentions", []):
        ci = ConversationInsight(conversation_id=conv.id, insight_type="budget_mention", content=item)
        db.add(ci)

    for item in analysis.get("competitor_mentions", []):
        ci = ConversationInsight(conversation_id=conv.id, insight_type="competitor_mention", content=item)
        db.add(ci)

    db.commit()

    return {
        "id": conv.id,
        "title": conv.title,
        "summary": conv.summary,
        "sentiment": conv.sentiment,
        "sentiment_score": conv.sentiment_score,
        "action_items": analysis.get("action_items", []),
        "budget_mentions": analysis.get("budget_mentions", []),
        "competitor_mentions": analysis.get("competitor_mentions", []),
    }
