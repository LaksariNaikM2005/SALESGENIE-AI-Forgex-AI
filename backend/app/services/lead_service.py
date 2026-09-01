from datetime import datetime

from ..extensions import db
from ai_ml_engine.inference.predict import predict_lead

from ..repositories.lead_repository import (
    create_lead,
    delete_lead,
    get_all_leads,
    get_lead_by_id,
    update_lead,
)


def serialize_lead(lead):
    return {
        "id": lead.id,
        "company": lead.company,
        "contact_name": lead.contact_name,
        "email": lead.email,
        "phone": lead.phone,
        "stage": lead.stage,
        "status": lead.status,
        "value": lead.value,
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
    return [serialize_lead(lead) for lead in get_all_leads()]


def find_lead(lead_id):
    lead = get_lead_by_id(lead_id)

    if not lead:
        return None

    return serialize_lead(lead)

def build_ml_input(data):
    """
    Convert API lead data into the feature structure
    expected by the trained ML model.
    """

    now = datetime.now()

    ml_data = {
        # Map CRM field to ML account feature.
        "account": data.get("account", data.get("company")),

        "sector": data.get("sector"),
        "year_established": data.get("year_established"),
        "revenue": data.get("revenue"),
        "employees": data.get("employees"),
        "office_location": data.get("office_location"),
        "subsidiary_of": data.get("subsidiary_of"),
        "product": data.get("product"),
        "series": data.get("series"),
        "sales_price": data.get("sales_price"),
        "sales_agent": data.get("sales_agent"),
        "manager": data.get("manager"),
        "regional_office": data.get("regional_office"),

        # Use current date when no engagement date
        # is supplied by the API.
        "engage_year": data.get(
            "engage_year",
            now.year,
        ),

        "engage_month": data.get(
            "engage_month",
            now.month,
        ),

        "engage_quarter": data.get(
            "engage_quarter",
            ((now.month - 1) // 3) + 1,
        ),

        "engage_dayofweek": data.get(
            "engage_dayofweek",
            now.weekday(),
        ),

        "account_age": data.get("account_age"),

        # Historical features.
        #
        # For a brand-new CRM lead there may be no
        # historical information available.
        # The training pipeline uses 0.5 as its
        # smoothed default and 0 previous deals.
        "historical_global_win_rate": data.get(
            "historical_global_win_rate",
            0.5,
        ),

        "historical_account_win_rate": data.get(
            "historical_account_win_rate",
            0.5,
        ),

        "historical_product_win_rate": data.get(
            "historical_product_win_rate",
            0.5,
        ),

        "historical_agent_win_rate": data.get(
            "historical_agent_win_rate",
            0.5,
        ),

        "historical_sector_win_rate": data.get(
            "historical_sector_win_rate",
            0.5,
        ),

        "account_previous_deals": data.get(
            "account_previous_deals",
            0,
        ),

        "product_previous_deals": data.get(
            "product_previous_deals",
            0,
        ),

        "agent_previous_deals": data.get(
            "agent_previous_deals",
            0,
        ),
    }

    return ml_data


def add_lead(data):
    """
    Create a lead, run ML prediction, save the prediction,
    and commit the complete lead transaction.
    """

    lead = create_lead(data)

    try:
        # Build the feature payload expected by the ML model.
        ml_input = build_ml_input(data)

        # Run prediction.
        prediction = predict_lead(ml_input)

        # Save ML results to the database record.
        lead.lead_score = prediction["lead_score"]
        lead.purchase_probability = prediction[
            "purchase_probability"
        ]

        # Commit lead + ML prediction together.
        db.session.commit()

    except Exception:
        # Roll back the uncommitted transaction if
        # ML prediction fails.
        db.session.rollback()
        raise

    return serialize_lead(lead)


def edit_lead(lead_id, data):
    lead = get_lead_by_id(lead_id)

    if not lead:
        return None

    lead = update_lead(lead, data)

    return serialize_lead(lead)


def remove_lead(lead_id):
    lead = get_lead_by_id(lead_id)

    if not lead:
        return False

    delete_lead(lead)

    return True
