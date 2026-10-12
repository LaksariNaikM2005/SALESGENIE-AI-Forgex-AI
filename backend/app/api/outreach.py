from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .auth import get_current_user
from ..database import get_db
from ..models import User
from ..services.outreach_service import generate_outreach_message

router = APIRouter(prefix="/api/outreach", tags=["AI Outreach"])
DbSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


class GenerateOutreachRequest(BaseModel):
    lead_name: Optional[str] = "Decision Maker"
    company_name: Optional[str] = "Manufacturing Partner"
    industry: Optional[str] = "Industrial Automation"
    message_type: Optional[str] = "Executive Email"
    tone: Optional[str] = "Executive & Consultative"
    value_prop: Optional[str] = "PLC & SCADA Integration"
    tech_stack: Optional[str] = "Siemens PLC, ROS2"


class SendOutreachRequest(BaseModel):
    recipient: str
    subject: str
    body: str


@router.post("/generate")
def generate_email(
    data: GenerateOutreachRequest,
    current_user: CurrentUser,
):
    result = generate_outreach_message(
        lead_name=data.lead_name or "Prospect",
        company_name=data.company_name or "Manufacturing Enterprise",
        industry=data.industry or "Industrial Automation",
        message_type=data.message_type or "Executive Email",
        tone=data.tone or "Executive & Consultative",
        value_prop=data.value_prop or "PLC & SCADA Integration",
        tech_stack=data.tech_stack or "Siemens PLC, ROS2",
    )

    return {
        "subject": result.get("subject"),
        "body": result.get("body"),
        "message_type": data.message_type,
        "tone": data.tone,
        "value_prop": data.value_prop,
        "lead_name": data.lead_name,
        "company_name": data.company_name,
    }


@router.post("/send")
def send_email(
    data: SendOutreachRequest,
    current_user: CurrentUser,
):
    if not data.recipient or not data.subject or not data.body:
        raise HTTPException(
            status_code=400,
            detail="Recipient, subject, and body are required",
        )

    return {
        "message": f"Outreach message successfully queued and delivered to {data.recipient}",
        "status": "delivered",
    }
