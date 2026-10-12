import logging
from pathlib import Path
import pandas as pd

from ..celery_app import celery_app
from ..database import SessionLocal
from ..models import Lead, AIRecommendation
from ..core.redis_client import redis_client
from ai_ml_engine.inference.predict import predict_lead

logger = logging.getLogger("celery_lead_tasks")


def build_ml_input_dict(lead: Lead) -> dict:
    return {
        "sector": getattr(lead, "sector", "Industrial Automation") or "Industrial Automation",
        "product": getattr(lead, "product", "Robotic Assembly Cell X7") or "Robotic Assembly Cell X7",
        "deal_stage": getattr(lead, "stage", "Qualified") or "Qualified",
        "sales_agent": getattr(lead, "sales_agent", "Marcus Vance") or "Marcus Vance",
        "deal_value": float(getattr(lead, "value", 125000.0) or 125000.0),
        "annual_revenue": float(getattr(lead, "revenue", 100.0) or 100.0),
        "employees": int(getattr(lead, "employees", 1000) or 1000),
    }


@celery_app.task(name="score_lead_task", bind=True)
def score_lead_task(self, lead_id: int):
    """
    Background job to run ML inference on a specific lead and update its qualification metrics.
    """
    session = SessionLocal()
    try:
        lead = session.get(Lead, lead_id)
        if not lead:
            logger.warning(f"Lead {lead_id} not found for scoring.")
            return {"status": "error", "message": f"Lead {lead_id} not found"}

        ml_input = build_ml_input_dict(lead)
        prediction = predict_lead(ml_input)

        lead.lead_score = float(prediction.get("lead_score", 75.0))
        lead.purchase_probability = float(prediction.get("purchase_probability", 0.75))
        session.commit()

        # Invalidate dashboard cache
        redis_client.delete_pattern("analytics:*")

        logger.info(f"Successfully scored lead {lead_id}: score={lead.lead_score}")
        return {
            "status": "success",
            "lead_id": lead_id,
            "lead_score": lead.lead_score,
            "purchase_probability": lead.purchase_probability,
        }
    except Exception as exc:
        session.rollback()
        logger.error(f"Error scoring lead {lead_id}: {exc}")
        return {"status": "error", "error": str(exc)}
    finally:
        session.close()


@celery_app.task(name="sync_dataset_task", bind=True)
def sync_dataset_task(self, file_path_str: str = None):
    """
    Heavy background job to ingest and score the 5,000 real-world manufacturing dataset records.
    """
    session = SessionLocal()
    try:
        project_root = Path(__file__).resolve().parents[3]
        dataset_path = (
            Path(file_path_str)
            if file_path_str
            else project_root / "ai_ml_engine" / "data" / "raw" / "sales_pipeline.csv"
        )

        if not dataset_path.exists():
            return {"status": "error", "message": f"File not found: {dataset_path}"}

        df = pd.read_csv(dataset_path)
        created_count = 0
        batch_size = 250

        for idx, row in df.iterrows():
            company = str(row["account"]).strip()
            contact = f"Agent {row['sales_agent']}"
            email = f"contact@{company.lower().replace(' ', '')}.com"
            value = float(row["deal_value"]) if pd.notna(row["deal_value"]) else 125000.0

            existing = session.query(Lead).filter_by(company=company, email=email).first()
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

                new_lead = Lead(
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
                session.add(new_lead)
                created_count += 1

                if created_count % batch_size == 0:
                    session.commit()

        session.commit()

        # Invalidate cache
        redis_client.delete_pattern("analytics:*")

        return {
            "status": "success",
            "imported_count": created_count,
            "total_leads": session.query(Lead).count(),
        }
    except Exception as exc:
        session.rollback()
        logger.error(f"Sync dataset task error: {exc}")
        return {"status": "error", "error": str(exc)}
    finally:
        session.close()
