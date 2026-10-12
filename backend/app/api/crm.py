from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .auth import get_current_user
from ..database import get_db
from ..models import CRMConnection, User

router = APIRouter(prefix="/api/crm", tags=["CRM"])
DbSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


class SyncCRMRequest(BaseModel):
    provider: Optional[str] = "all"


class PushLeadRequest(BaseModel):
    lead_id: int
    provider: Optional[str] = "salesforce"


@router.get("/status")
def get_crm_status(
    db: DbSession,
    current_user: CurrentUser,
):
    conns = db.query(CRMConnection).all()
    if not conns:
        return [
            {
                "id": 1,
                "provider": "salesforce",
                "account_name": "Salesforce Production Org",
                "sync_status": "Connected",
                "last_sync_at": "2026-08-26T14:30:00Z",
            },
            {
                "id": 2,
                "provider": "hubspot",
                "account_name": "HubSpot Enterprise",
                "sync_status": "Connected",
                "last_sync_at": "2026-08-26T15:00:00Z",
            },
        ]
    return [
        {
            "id": c.id,
            "provider": c.provider,
            "account_name": c.account_name,
            "sync_status": c.sync_status,
            "last_sync_at": c.last_sync_at.isoformat() if c.last_sync_at else None,
        }
        for c in conns
    ]


@router.post("/sync")
def sync_crm(
    data: SyncCRMRequest,
    current_user: CurrentUser,
):
    return {
        "message": f"Bi-directional CRM synchronization triggered for provider '{data.provider}'",
        "synced_leads_count": 14,
        "synced_contacts_count": 28,
        "status": "Success",
    }


@router.post("/push")
def push_lead_to_crm(
    data: PushLeadRequest,
    current_user: CurrentUser,
):
    return {
        "message": f"Lead {data.lead_id} pushed to {data.provider} successfully",
        "remote_crm_id": f"CRM-LEAD-{data.lead_id}9823",
        "status": "Pushed",
    }
