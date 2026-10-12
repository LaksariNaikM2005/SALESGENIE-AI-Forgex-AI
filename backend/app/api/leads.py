import math
from pathlib import Path
from typing import Annotated, Optional
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import or_
from sqlalchemy.orm import Session

from .auth import get_current_user, require_admin, require_manager_or_admin
from ..database import get_db
from ..models import Lead, User
from ..core.redis_client import redis_client
from ..services.lead_service import auto_seed_leads_if_empty, serialize_lead, build_ml_input
from ..tasks.lead_tasks import score_lead_task, sync_dataset_task
from ai_ml_engine.inference.predict import predict_lead

router = APIRouter(prefix="/api/leads", tags=["Leads"])
DbSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]
AdminUser = Annotated[User, Depends(require_admin)]
ManagerUser = Annotated[User, Depends(require_manager_or_admin)]

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RAW_PIPELINE_PATH = PROJECT_ROOT / "ai_ml_engine" / "data" / "raw" / "sales_pipeline.csv"


class CreateLeadRequest(BaseModel):
    company: str
    contact_name: Optional[str] = "Decision Maker"
    email: Optional[str] = None
    phone: Optional[str] = None
    stage: Optional[str] = "New Lead"
    status: Optional[str] = "Open"
    value: Optional[float] = 125000.0
    sector: Optional[str] = "Industrial Automation"
    product: Optional[str] = "Robotic Assembly Cell X7"
    tech_stack: Optional[str] = "ROS2, Siemens PLC, Fanuc CNC"
    revenue: Optional[float] = 85.0
    employees: Optional[int] = 1450
    sales_agent: Optional[str] = "Marcus Vance"


class UpdateLeadRequest(BaseModel):
    company: Optional[str] = None
    contact_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    stage: Optional[str] = None
    status: Optional[str] = None
    value: Optional[float] = None
    sector: Optional[str] = None
    product: Optional[str] = None
    tech_stack: Optional[str] = None
    revenue: Optional[float] = None
    employees: Optional[int] = None
    sales_agent: Optional[str] = None
    lead_score: Optional[float] = None
    purchase_probability: Optional[float] = None


@router.get("")
def list_leads(
    db: DbSession,
    current_user: CurrentUser,
    search: Optional[str] = Query(None),
    sector: Optional[str] = Query(None),
    stage: Optional[str] = Query(None),
    page: Optional[int] = Query(None, ge=1),
    per_page: Optional[int] = Query(None, ge=1),
):
    auto_seed_leads_if_empty()

    query = db.query(Lead)

    if search:
        s = f"%{search.strip().lower()}%"
        query = query.filter(
            or_(
                Lead.company.ilike(s),
                Lead.contact_name.ilike(s),
                Lead.email.ilike(s),
            )
        )

    if sector and sector.lower() != "all":
        query = query.filter(Lead.sector.ilike(f"%{sector.strip()}%"))

    if stage and stage.lower() != "all":
        query = query.filter(Lead.stage.ilike(f"%{stage.strip()}%"))

    total_count = query.count()

    if page and per_page:
        leads_objs = (
            query.order_by(Lead.id.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )
        total_pages = math.ceil(total_count / per_page) if per_page > 0 else 1
        return {
            "leads": [serialize_lead(l) for l in leads_objs],
            "total": total_count,
            "page": page,
            "per_page": per_page,
            "pages": total_pages,
        }

    leads_objs = query.order_by(Lead.id.desc()).all()
    return {
        "leads": [serialize_lead(l) for l in leads_objs],
        "total": total_count,
    }


@router.post("", status_code=201)
def create_lead(
    data: CreateLeadRequest,
    db: DbSession,
    current_user: CurrentUser,
):
    if not data.company or not data.company.strip():
        raise HTTPException(status_code=400, detail="company is required")

    lead_dict = data.model_dump()
    ml_input = build_ml_input(lead_dict)
    prediction = predict_lead(ml_input)

    new_lead = Lead(
        company=data.company.strip(),
        contact_name=data.contact_name,
        email=data.email,
        phone=data.phone,
        stage=data.stage or "New Lead",
        status=data.status or "Open",
        value=data.value or 0.0,
        sector=data.sector or "Industrial Automation",
        product=data.product or "Robotic Assembly Cell X7",
        tech_stack=data.tech_stack or "ROS2, Siemens PLC, Fanuc CNC",
        revenue=data.revenue or 85.0,
        employees=data.employees or 1450,
        sales_agent=data.sales_agent or current_user.name,
        assigned_to=current_user.id,
        lead_score=prediction.get("lead_score", 75.0),
        purchase_probability=prediction.get("purchase_probability", 0.75),
    )

    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)

    # Invalidate Redis cache
    redis_client.delete_pattern("analytics:*")

    return {
        "message": "Lead created successfully",
        "lead": serialize_lead(new_lead),
    }


@router.get("/{lead_id}")
def get_lead(
    lead_id: int,
    db: DbSession,
    current_user: CurrentUser,
):
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"lead": serialize_lead(lead)}


@router.put("/{lead_id}")
def update_lead(
    lead_id: int,
    data: UpdateLeadRequest,
    db: DbSession,
    current_user: CurrentUser,
):
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, val in update_data.items():
        if hasattr(lead, field):
            setattr(lead, field, val)

    db.commit()
    db.refresh(lead)

    redis_client.delete_pattern("analytics:*")

    return {
        "message": "Lead updated successfully",
        "lead": serialize_lead(lead),
    }


@router.delete("/{lead_id}")
def delete_lead(
    lead_id: int,
    db: DbSession,
    manager: ManagerUser,
):
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    db.delete(lead)
    db.commit()

    redis_client.delete_pattern("analytics:*")
    return {"message": "Lead deleted successfully"}


@router.post("/{lead_id}/score")
def score_lead(
    lead_id: int,
    db: DbSession,
    current_user: CurrentUser,
    use_celery: bool = Query(False, description="Run async in Celery worker"),
):
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    if use_celery:
        try:
            task = score_lead_task.delay(lead_id)
            return {
                "message": "Scoring job queued in Celery background worker",
                "task_id": task.id,
                "status": "QUEUED",
            }
        except Exception:
            # Fall back to synchronous scoring
            pass

    ml_input = build_ml_input(lead)
    prediction = predict_lead(ml_input)

    lead.lead_score = prediction["lead_score"]
    lead.purchase_probability = prediction["purchase_probability"]
    db.commit()
    db.refresh(lead)

    redis_client.delete_pattern("analytics:*")

    return {
        "lead_id": lead_id,
        "lead_score": lead.lead_score,
        "purchase_probability": lead.purchase_probability,
        "prediction": prediction.get("prediction", 1),
    }


@router.post("/sync-real-dataset")
def sync_real_dataset(
    db: DbSession,
    admin: AdminUser,
    use_celery: bool = Query(False, description="Dispatch to Celery worker"),
):
    if not RAW_PIPELINE_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Raw dataset not found at: {RAW_PIPELINE_PATH}",
        )

    if use_celery:
        try:
            task = sync_dataset_task.delay(str(RAW_PIPELINE_PATH))
            return {
                "message": "Dataset synchronization dispatched to Celery background worker",
                "task_id": task.id,
                "status": "PROCESSING",
            }
        except Exception:
            pass

    # Direct synchronous ingestion
    df = pd.read_csv(RAW_PIPELINE_PATH)
    created_count = 0
    batch_size = 500

    for idx, row in df.iterrows():
        company = str(row["account"]).strip()
        contact = f"Agent {row['sales_agent']}"
        email = f"contact@{company.lower().replace(' ', '')}.com"
        value = float(row["deal_value"]) if pd.notna(row["deal_value"]) else 125000.0

        existing = db.query(Lead).filter_by(company=company, email=email).first()
        if not existing:
            lead_data = {
                "sector": str(row["sector"]).strip(),
                "product": str(row["product"]).strip(),
                "deal_stage": "Won" if str(row["deal_stage"]).strip().lower() == "won" else "Qualified",
                "sales_agent": str(row["sales_agent"]).strip(),
                "deal_value": value,
                "annual_revenue": float(row["revenue"]) if pd.notna(row["revenue"]) else 100.0,
                "employees": int(row["employees"]) if pd.notna(row["employees"]) else 1000,
            }
            pred = predict_lead(lead_data)

            lead = Lead(
                company=company,
                contact_name=contact,
                email=email,
                value=value,
                stage=lead_data["deal_stage"],
                status="Open",
                sector=lead_data["sector"],
                product=lead_data["product"],
                sales_agent=lead_data["sales_agent"],
                revenue=lead_data["annual_revenue"],
                employees=lead_data["employees"],
                lead_score=pred["lead_score"],
                purchase_probability=pred["purchase_probability"],
            )
            db.add(lead)
            created_count += 1

            if created_count % batch_size == 0:
                db.commit()

    db.commit()
    redis_client.delete_pattern("analytics:*")

    return {
        "message": f"Successfully synchronized {created_count} real-world records into PostgreSQL/Database.",
        "total_leads_in_db": db.query(Lead).count(),
    }
