from datetime import datetime, timezone
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .auth import get_current_user
from ..database import get_db
from ..models import FollowUpHistory, Lead, User

router = APIRouter(prefix="/api/followups", tags=["Follow-ups"])
DbSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


class CreateFollowUpRequest(BaseModel):
    lead_id: int
    scheduled_at: Optional[str] = None
    follow_up_type: Optional[str] = "Call"
    channel: Optional[str] = "Phone"
    priority: Optional[str] = "Medium"
    notes: Optional[str] = None


class UpdateFollowUpRequest(BaseModel):
    scheduled_at: Optional[str] = None
    completed: Optional[bool] = None
    notes: Optional[str] = None
    status: Optional[str] = None
    outcome: Optional[str] = None


def serialize_followup(f: FollowUpHistory) -> dict:
    lead = f.lead
    return {
        "id": f.id,
        "lead_id": f.lead_id,
        "lead_company": lead.company if lead else "Manufacturing Lead",
        "lead_contact": lead.contact_name if lead else "Contact",
        "sector": getattr(lead, "sector", "Industrial Automation") if lead else "Industrial Automation",
        "follow_up_type": getattr(f, "follow_up_type", "Call") or "Call",
        "channel": getattr(f, "channel", "Phone") or "Phone",
        "scheduled_at": f.scheduled_at.isoformat() if getattr(f, "scheduled_at", None) else None,
        "completed_at": f.completed_at.isoformat() if getattr(f, "completed_at", None) else None,
        "completed": getattr(f, "completed", False),
        "notes": f.notes,
        "status": getattr(f, "status", "Pending") or "Pending",
        "priority": getattr(f, "priority", "Medium") or "Medium",
    }


@router.get("")
def list_followups(
    db: DbSession,
    current_user: CurrentUser,
    status: Optional[str] = Query(None),
):
    query = db.query(FollowUpHistory)
    if status and status.lower() != "all":
        query = query.filter_by(status=status)

    followups = query.order_by(FollowUpHistory.id.desc()).all()
    return {
        "followups": [serialize_followup(f) for f in followups],
        "total": len(followups),
    }


@router.post("", status_code=201)
def create_followup(
    data: CreateFollowUpRequest,
    db: DbSession,
    current_user: CurrentUser,
):
    lead = db.get(Lead, data.lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    new_fu = FollowUpHistory(
        lead_id=data.lead_id,
        notes=data.notes,
        scheduled_at=datetime.now(timezone.utc),
        status="Pending",
        completed=False,
    )
    if hasattr(new_fu, "channel"):
        new_fu.channel = data.channel
    if hasattr(new_fu, "priority"):
        new_fu.priority = data.priority
    if hasattr(new_fu, "follow_up_type"):
        new_fu.follow_up_type = data.follow_up_type

    db.add(new_fu)
    db.commit()
    db.refresh(new_fu)

    return {
        "message": "Follow-up scheduled successfully",
        "followup": serialize_followup(new_fu),
    }


@router.put("/{followup_id}")
def update_followup(
    followup_id: int,
    data: UpdateFollowUpRequest,
    db: DbSession,
    current_user: CurrentUser,
):
    fu = db.get(FollowUpHistory, followup_id)
    if not fu:
        raise HTTPException(status_code=404, detail="Follow-up not found")

    if data.completed is not None:
        fu.completed = data.completed
        if data.completed:
            fu.status = "Completed"
            fu.completed_at = datetime.now(timezone.utc)
    if data.notes is not None:
        fu.notes = data.notes
    if data.status is not None:
        fu.status = data.status

    db.commit()
    db.refresh(fu)
    return {
        "message": "Follow-up updated successfully",
        "followup": serialize_followup(fu),
    }


@router.delete("/{followup_id}")
def delete_followup(
    followup_id: int,
    db: DbSession,
    current_user: CurrentUser,
):
    fu = db.get(FollowUpHistory, followup_id)
    if not fu:
        raise HTTPException(status_code=404, detail="Follow-up not found")

    db.delete(fu)
    db.commit()
    return {"message": "Follow-up deleted successfully"}
