import math
from pathlib import Path
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
import pandas as pd

from ..extensions import db
from ..models import Lead
from ..services.lead_service import (
    add_lead,
    auto_seed_leads_if_empty,
    build_ml_input,
    edit_lead,
    find_lead,
    list_leads,
    remove_lead,
    serialize_lead,
)
from ..utils.decorators import role_required
from ai_ml_engine.inference.predict import predict_lead

leads_bp = Blueprint("leads", __name__, url_prefix="/api/leads")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
RAW_PIPELINE_PATH = PROJECT_ROOT / "ai_ml_engine" / "data" / "raw" / "sales_pipeline.csv"


@leads_bp.post("")
@jwt_required()
def create():
    data = request.get_json() or {}

    if not data.get("company"):
        return {"error": "company is required"}, 400

    try:
        lead = add_lead(data)
        return {
            "message": "Lead created successfully",
            "lead": lead,
        }, 201
    except (TypeError, ValueError) as exc:
        return {"error": str(exc)}, 400


@leads_bp.get("")
@jwt_required()
def get_all():
    # Guarantee manufacturing dataset leads are auto-seeded if database empty
    auto_seed_leads_if_empty()

    search = request.args.get("search", "").strip().lower()
    sector_filter = request.args.get("sector", "").strip().lower()
    stage_filter = request.args.get("stage", "").strip().lower()
    page = request.args.get("page", type=int)
    per_page = request.args.get("per_page", type=int)

    query = Lead.query

    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Lead.company.ilike(search_filter))
            | (Lead.contact_name.ilike(search_filter))
            | (Lead.email.ilike(search_filter))
        )

    if sector_filter and sector_filter != "all":
        query = query.filter(Lead.sector.ilike(f"%{sector_filter}%"))

    if stage_filter and stage_filter != "all":
        query = query.filter(Lead.stage.ilike(f"%{stage_filter}%"))

    total_count = query.count()

    if page and per_page:
        leads_objs = (
            query.order_by(Lead.id.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )
        total_pages = math.ceil(total_count / per_page) if per_page > 0 else 1
        return jsonify({
            "leads": [serialize_lead(l) for l in leads_objs],
            "total": total_count,
            "page": page,
            "per_page": per_page,
            "pages": total_pages,
        }), 200

    leads_objs = query.order_by(Lead.id.desc()).all()
    return jsonify({
        "leads": [serialize_lead(l) for l in leads_objs],
        "total": total_count,
    }), 200


@leads_bp.post("/sync-real-dataset")
@role_required("admin")
def sync_real_dataset():
    """
    Populates all 5,000 real-world sales pipeline records into the application database.
    Restricted to System Administrators only.
    """
    if not RAW_PIPELINE_PATH.exists():
        return jsonify({"error": f"Raw dataset not found at: {RAW_PIPELINE_PATH}"}), 404

    df = pd.read_csv(RAW_PIPELINE_PATH)

    created_count = 0
    batch_size = 500

    for idx, row in df.iterrows():
        company = str(row["account"]).strip()
        contact = f"Agent {row['sales_agent']}"
        email = f"contact@{company.lower().replace(' ', '')}.com"
        value = float(row["deal_value"]) if pd.notna(row["deal_value"]) else 125000.0

        existing = Lead.query.filter_by(company=company, email=email).first()
        if not existing:
            lead_data = {
                "company": company,
                "contact_name": contact,
                "email": email,
                "value": value,
                "stage": "Won" if str(row["deal_stage"]).strip().lower() == "won" else "Qualified",
                "sector": str(row["sector"]).strip(),
                "product": str(row["product"]).strip(),
                "sales_agent": str(row["sales_agent"]).strip(),
                "revenue": float(row["revenue"]) if pd.notna(row["revenue"]) else 100.0,
                "employees": int(row["employees"]) if pd.notna(row["employees"]) else 1000,
            }

            ml_input = build_ml_input(lead_data)
            prediction = predict_lead(ml_input)

            lead = Lead(
                company=company,
                contact_name=contact,
                email=email,
                value=value,
                stage=lead_data["stage"],
                status="Open",
                lead_score=prediction["lead_score"],
                purchase_probability=prediction["purchase_probability"],
            )
            db.session.add(lead)
            created_count += 1

            if created_count % batch_size == 0:
                db.session.commit()

    db.session.commit()

    from ..services.ai_service import generate_all_recommendations
    generate_all_recommendations()

    return jsonify({
        "message": f"Successfully synchronized {created_count} real-world dataset records into database.",
        "total_leads_in_db": Lead.query.count(),
    }), 200


@leads_bp.get("/<int:lead_id>")
@jwt_required()
def get_one(lead_id):
    lead = find_lead(lead_id)
    if not lead:
        return {"error": "Lead not found"}, 404
    return {"lead": lead}, 200


@leads_bp.put("/<int:lead_id>")
@jwt_required()
def update(lead_id):
    data = request.get_json() or {}
    try:
        lead = edit_lead(lead_id, data)
        if not lead:
            return {"error": "Lead not found"}, 404
        return {
            "message": "Lead updated successfully",
            "lead": lead,
        }, 200
    except (TypeError, ValueError) as exc:
        return {"error": str(exc)}, 400


@leads_bp.delete("/<int:lead_id>")
@role_required("sales_manager")
def delete(lead_id):
    deleted = remove_lead(lead_id)
    if not deleted:
        return {"error": "Lead not found"}, 404
    return {"message": "Lead deleted successfully"}, 200


@leads_bp.post("/<int:lead_id>/score")
@jwt_required()
def score_lead(lead_id):
    lead_obj = find_lead(lead_id)
    if not lead_obj:
        return {"error": "Lead not found"}, 404

    ml_input = build_ml_input(lead_obj)
    prediction = predict_lead(ml_input)

    edit_lead(lead_id, {
        "lead_score": prediction["lead_score"],
        "purchase_probability": prediction["purchase_probability"],
    })

    return {
        "lead_id": lead_id,
        "lead_score": prediction["lead_score"],
        "purchase_probability": prediction["purchase_probability"],
        "prediction": prediction["prediction"],
    }, 200
