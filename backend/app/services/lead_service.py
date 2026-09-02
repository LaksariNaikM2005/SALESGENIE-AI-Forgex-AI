from datetime import datetime
import logging
from pathlib import Path
import pandas as pd

from ..extensions import db
from ..models import Lead
from ai_ml_engine.inference.predict import predict_lead

from ..repositories.lead_repository import (
    create_lead,
    delete_lead,
    get_all_leads,
    get_lead_by_id,
    update_lead,
)

logger = logging.getLogger(__name__)


def safe_float(val, default=0.0) -> float:
    if val is None:
        return float(default)
    try:
        return float(val)
    except (ValueError, TypeError):
        return float(default)


def safe_int(val, default=0) -> int:
    if val is None:
        return int(default)
    try:
        return int(val)
    except (ValueError, TypeError):
        return int(default)


def auto_seed_leads_if_empty():
    """
    Guarantees that real-world manufacturing dataset leads and connected AI recommendations
    are populated dynamically if database leads table is empty.
    Loads all records from the real-world sales_pipeline.csv dataset.
    """
    from werkzeug.security import generate_password_hash
    from ..models import User

    # Ensure demo users exist
    if User.query.count() == 0:
        demo_users = [
            {"name": "Admin User",     "email": "admin@forgex.ai",   "password": "Admin@123",   "role": "admin"},
            {"name": "Sarah Mitchell", "email": "manager@forgex.ai", "password": "Manager@123", "role": "sales_manager"},
            {"name": "James Carter",   "email": "sales@forgex.ai",   "password": "Sales@123",   "role": "sales_rep"},
            {"name": "Priya Sharma",   "email": "priya@forgex.ai",   "password": "Priya@123",   "role": "sales_rep"},
            {"name": "Marcus Vance",   "email": "marcus@forgex.ai",  "password": "Marcus@123",  "role": "sales_rep"},
        ]
        for ud in demo_users:
            if not User.query.filter_by(email=ud["email"]).first():
                db.session.add(User(
                    name=ud["name"],
                    email=ud["email"],
                    password_hash=generate_password_hash(ud["password"]),
                    role=ud["role"],
                    is_active=True,
                ))
        db.session.commit()

    if Lead.query.count() > 0:
        return

    project_root = Path(__file__).resolve().parent.parent.parent.parent
    raw_path = project_root / "ai_ml_engine" / "data" / "raw" / "sales_pipeline.csv"

    if not raw_path.exists():
        logger.warning(f"Dataset not found at {raw_path}. Cannot auto-seed leads.")
        return

    TECH_STACK_MAP = {
        "semi": "EUV Lithography, MES, Cleanroom SCADA, APC",
        "auto": "Automotive Stamping, ROS2, Vision Inspection, MES",
        "tool": "Fanuc CNC, High-Speed Spindles, CAD/CAM",
        "cnc":  "Fanuc CNC, High-Speed Spindles, CAD/CAM",
        "heavy": "Siemens S7 PLC, Heavy Hydraulics, SCADA",
        "elec": "PCB Assembly Line, AOI Systems, SMT Equipment",
        "robot": "KUKA Robots, ROS2, Force/Torque Sensors",
        "food": "HACCP Systems, Conveyor Automation, ERP",
        "pharm": "FDA-Compliant MES, Clean Room HVAC, Serialization",
    }

    def get_tech_stack(sector):
        s = str(sector).lower()
        for key, stack in TECH_STACK_MAP.items():
            if key in s:
                return stack
        return "ROS2, Siemens S7 PLC, Fanuc CNC, IoT Edge"

    def map_stage(deal_stage):
        s = str(deal_stage).strip().lower()
        if s == "won":           return "Won"
        if s == "lost":          return "Lost"
        if s == "proposal":      return "Proposal"
        if s == "negotiation":   return "Negotiation"
        if s == "qualified":     return "Qualified"
        return "New Lead"

    try:
        df = pd.read_csv(raw_path)
    except Exception as e:
        logger.error(f"Failed to read dataset CSV: {e}")
        return

    created = 0
    errors = 0
    batch_size = 200

    for idx, row in df.iterrows():
        try:
            company    = str(row.get("account", f"Company_{idx}")).strip()
            agent      = str(row.get("sales_agent", "Marcus Vance")).strip()
            sector     = str(row.get("sector", "industrial_automation")).strip()
            product    = str(row.get("product", "Industrial Robot")).strip()
            deal_stage = str(row.get("deal_stage", "Qualified")).strip()
            revenue    = safe_float(row.get("revenue"), default=85.0)
            employees  = safe_int(row.get("employees"), default=1450)
            deal_val   = safe_float(row.get("deal_value"), default=125000.0)
            sector_clean = sector.replace("_", " ").title()
            email = f"contact.{idx}@{company.lower().replace(' ', '').replace('.', '')}.com"

            lead_payload = {
                "account": company,
                "company": company,
                "sector": sector,
                "product": product,
                "sales_agent": agent,
                "manager": str(row.get("manager", "Alex Vance")).strip(),
                "regional_office": str(row.get("regional_office", "Midwest")).strip(),
                "revenue": revenue,
                "employees": employees,
                "value": deal_val,
                "sales_price": safe_float(row.get("sales_price"), default=deal_val),
                "year_established": safe_int(row.get("year_established"), default=1998),
                "office_location": str(row.get("office_location", "United States")).strip(),
                "series": str(row.get("series", "Industrial Automation")).strip(),
            }

            ml_input = build_ml_input(lead_payload)
            prediction = predict_lead(ml_input)
            stage = map_stage(deal_stage)

            lead = Lead(
                company=company,
                contact_name=f"Contact at {company}",
                email=email,
                value=deal_val,
                sector=sector_clean,
                product=product,
                tech_stack=get_tech_stack(sector),
                revenue=revenue,
                employees=employees,
                sales_agent=agent,
                stage=stage,
                status="Open" if stage not in ["Won", "Lost"] else "Closed",
                lead_score=prediction["lead_score"],
                purchase_probability=prediction["purchase_probability"],
            )
            db.session.add(lead)
            created += 1

            if created % batch_size == 0:
                db.session.commit()
                logger.info(f"Auto-seed: committed {created} leads so far...")

        except Exception as exc:
            errors += 1
            if errors <= 5:
                logger.error(f"Auto-seed row {idx} error: {exc}")

    db.session.commit()
    logger.info(f"Auto-seed complete: {created} leads created ({errors} errors)")

    # Connect AI Recommendations to every seeded lead
    try:
        from .ai_service import generate_all_recommendations
        generate_all_recommendations()
        logger.info("Auto-seed: AI recommendations generated for all leads")
    except Exception as e:
        logger.error(f"Auto-seed: failed to generate AI recommendations: {e}")



def serialize_lead(lead):
    tech_stack = getattr(lead, "tech_stack", None)
    if not tech_stack and getattr(lead, "company_rel", None):
        tech_stack = lead.company_rel.technology_stack

    if not tech_stack:
        sector_str = str(getattr(lead, "sector", "")).lower()
        if "semi" in sector_str:
            tech_stack = "EUV Lithography, MES, Cleanroom Automation"
        elif "auto" in sector_str:
            tech_stack = "Automotive Stamping, ROS2, AI Vision Inspection"
        elif "tooling" in sector_str or "cnc" in sector_str:
            tech_stack = "Fanuc CNC, High-Speed Spindles, CAD/CAM"
        elif "heavy" in sector_str:
            tech_stack = "Siemens S7 PLC, SCADA, Heavy Hydraulics"
        else:
            tech_stack = "ROS2, Siemens PLC, Fanuc CNC, IoT Edge"

    return {
        "id": lead.id,
        "company": lead.company,
        "contact_name": lead.contact_name,
        "email": lead.email,
        "phone": lead.phone,
        "stage": lead.stage,
        "status": lead.status,
        "value": lead.value,
        "sector": getattr(lead, "sector", None) or "Industrial Automation",
        "product": getattr(lead, "product", None) or "Robotic Assembly Cell X7",
        "tech_stack": tech_stack,
        "revenue": getattr(lead, "revenue", None) or 85.0,
        "employees": getattr(lead, "employees", None) or 1450,
        "sales_agent": getattr(lead, "sales_agent", None) or "Marcus Vance",
        "lead_score": lead.lead_score,
        "purchase_probability": lead.purchase_probability,
        "last_contact_at": (
            lead.last_contact_at.isoformat()
            if lead.last_contact_at
            else None
        ),
        "response_time": lead.response_time,
        "sales_cycle": lead.sales_cycle,
        "assigned_to": lead.assigned_to,
        "created_at": (
            lead.created_at.isoformat()
            if lead.created_at
            else None
        ),
        "updated_at": (
            lead.updated_at.isoformat()
            if lead.updated_at
            else None
        ),
    }


def list_leads():
    auto_seed_leads_if_empty()
    return [serialize_lead(lead) for lead in get_all_leads()]


def find_lead(lead_id):
    auto_seed_leads_if_empty()
    lead = get_lead_by_id(lead_id)
    if not lead:
        return None
    return serialize_lead(lead)


def build_ml_input(data: dict) -> dict:
    now = datetime.now()

    value = safe_float(data.get("value"), default=125000.0)
    sales_price = safe_float(data.get("sales_price"), default=value)
    revenue = safe_float(data.get("revenue"), default=(value / 1000.0) if value > 1000 else 85.0)
    employees = safe_int(data.get("employees"), default=1450)
    cycle_days = safe_float(data.get("deal_cycle_days") or data.get("sales_cycle"), default=30.0)

    ml_data = {
        "account": data.get("account") or data.get("company") or "Apex Precision Robotics",
        "sector": data.get("sector") or "industrial_automation",
        "year_established": safe_int(data.get("year_established"), default=1998),
        "revenue": revenue,
        "employees": employees,
        "office_location": data.get("office_location") or "United States",
        "subsidiary_of": data.get("subsidiary_of"),
        "product": data.get("product") or "Robotic Assembly Cell X7",
        "series": data.get("series") or "Industrial Automation",
        "sales_price": sales_price,
        "sales_agent": data.get("sales_agent") or "Marcus Vance",
        "manager": data.get("manager") or "Alex Vance",
        "regional_office": data.get("regional_office") or "Midwest Region",
        "engage_year": safe_int(data.get("engage_year"), default=now.year),
        "engage_month": safe_int(data.get("engage_month"), default=now.month),
        "engage_quarter": safe_int(data.get("engage_quarter"), default=((now.month - 1) // 3) + 1),
        "engage_dayofweek": safe_int(data.get("engage_dayofweek"), default=now.weekday()),
        "account_age": safe_int(data.get("account_age"), default=26),
        "deal_cycle_days": cycle_days,
        "price_ratio": round(value / (sales_price + 1e-5), 4),
        "revenue_per_employee": round(revenue / (employees + 1), 4),
        "historical_global_win_rate": safe_float(data.get("historical_global_win_rate"), default=0.54),
        "historical_account_win_rate": safe_float(data.get("historical_account_win_rate"), default=0.50),
        "historical_product_win_rate": safe_float(data.get("historical_product_win_rate"), default=0.50),
        "historical_agent_win_rate": safe_float(data.get("historical_agent_win_rate"), default=0.50),
        "historical_sector_win_rate": safe_float(data.get("historical_sector_win_rate"), default=0.50),
        "account_previous_deals": safe_int(data.get("account_previous_deals"), default=0),
        "product_previous_deals": safe_int(data.get("product_previous_deals"), default=0),
        "agent_previous_deals": safe_int(data.get("agent_previous_deals"), default=0),
    }

    return ml_data


def add_lead(data: dict):
    lead = create_lead(data)

    if "sector" in data:
        lead.sector = data["sector"]
    if "product" in data:
        lead.product = data["product"]
    if "tech_stack" in data:
        lead.tech_stack = data["tech_stack"]
    if "revenue" in data:
        lead.revenue = safe_float(data["revenue"], 85.0)
    if "employees" in data:
        lead.employees = safe_int(data["employees"], 1450)
    if "sales_agent" in data:
        lead.sales_agent = data["sales_agent"]

    try:
        ml_input = build_ml_input(data)
        prediction = predict_lead(ml_input)

        lead.lead_score = prediction["lead_score"]
        lead.purchase_probability = prediction["purchase_probability"]

        db.session.commit()

        # Connect an AI recommendation for new lead
        from .ai_service import create_recommendation
        create_recommendation(lead.id)

    except Exception as exc:
        logger.error(f"Error executing ML inference for lead creation: {exc}")
        db.session.rollback()
        raise

    return serialize_lead(lead)


def edit_lead(lead_id: int, data: dict):
    lead = get_lead_by_id(lead_id)
    if not lead:
        return None

    lead = update_lead(lead, data)
    return serialize_lead(lead)


def remove_lead(lead_id: int) -> bool:
    lead = get_lead_by_id(lead_id)
    if not lead:
        return False

    delete_lead(lead)
    return True
