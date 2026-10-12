from typing import Annotated, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .auth import get_current_user
from ..database import get_db
from ..models import AIRecommendation, Lead, User
from ..services.lead_service import auto_seed_leads_if_empty
from ..services.ai_service import generate_all_recommendations

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])
DbSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


class UpdateRecommendationRequest(BaseModel):
    completed: Optional[bool] = None
    priority: Optional[str] = None
    reason: Optional[str] = None


def serialize_rec(r: AIRecommendation) -> dict:
    lead = r.lead
    return {
        "id": r.id,
        "lead_id": r.lead_id,
        "lead_company": lead.company if lead else "General Prospect",
        "lead_contact": lead.contact_name if lead else "Decision Maker",
        "sector": getattr(lead, "sector", "Industrial Automation") if lead else "Industrial Automation",
        "lead_score": getattr(lead, "lead_score", 85.0) if lead else 85.0,
        "purchase_probability": getattr(lead, "purchase_probability", 0.75) if lead else 0.75,
        "stage": getattr(lead, "stage", "Qualified") if lead else "Qualified",
        "recommendation": r.recommendation,
        "priority": r.priority,
        "reason": r.reason,
        "completed": r.completed,
        "generated_at": r.generated_at.isoformat() if r.generated_at else None,
    }


@router.get("")
def get_recommendations(
    db: DbSession,
    current_user: CurrentUser,
    priority: Optional[str] = Query(None),
):
    auto_seed_leads_if_empty()

    query = db.query(AIRecommendation)
    if priority and priority.lower() != "all":
        query = query.filter_by(priority=priority)

    recs = query.order_by(AIRecommendation.generated_at.desc()).all()

    if not recs:
        generate_all_recommendations()
        recs = db.query(AIRecommendation).order_by(AIRecommendation.generated_at.desc()).all()

    return {
        "recommendations": [serialize_rec(r) for r in recs],
        "total": len(recs),
    }


@router.put("/{rec_id}")
def update_recommendation(
    rec_id: int,
    data: UpdateRecommendationRequest,
    db: DbSession,
    current_user: CurrentUser,
):
    rec = db.get(AIRecommendation, rec_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    if data.completed is not None:
        rec.completed = data.completed
    if data.priority is not None:
        rec.priority = data.priority
    if data.reason is not None:
        rec.reason = data.reason

    db.commit()
    db.refresh(rec)
    return {
        "message": "Recommendation updated",
        "recommendation": serialize_rec(rec),
    }


@router.delete("/{rec_id}")
def delete_recommendation(
    rec_id: int,
    db: DbSession,
    current_user: CurrentUser,
):
    rec = db.get(AIRecommendation, rec_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    db.delete(rec)
    db.commit()
    return {"message": "Recommendation deleted"}
