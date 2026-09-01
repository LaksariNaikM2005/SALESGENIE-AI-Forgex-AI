from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from ..services.lead_service import (
    add_lead,
    edit_lead,
    find_lead,
    list_leads,
    remove_lead,
)


leads_bp = Blueprint(
    "leads",
    __name__,
    url_prefix="/api/leads",
)


@leads_bp.post("")
@jwt_required()
def create():
    data = request.get_json() or {}

    if not data.get("company"):
        return {
            "error": "company is required"
        }, 400

    try:
        lead = add_lead(data)

        return {
            "message": "Lead created successfully",
            "lead": lead,
        }, 201

    except (TypeError, ValueError) as exc:
        return {
            "error": str(exc)
        }, 400


@leads_bp.get("")
@jwt_required()
def get_all():
    return {
        "leads": list_leads()
    }, 200


@leads_bp.get("/<int:lead_id>")
@jwt_required()
def get_one(lead_id):
    lead = find_lead(lead_id)

    if not lead:
        return {
            "error": "Lead not found"
        }, 404

    return {
        "lead": lead
    }, 200


@leads_bp.put("/<int:lead_id>")
@jwt_required()
def update(lead_id):
    data = request.get_json() or {}

    try:
        lead = edit_lead(lead_id, data)

        if not lead:
            return {
                "error": "Lead not found"
            }, 404

        return {
            "message": "Lead updated successfully",
            "lead": lead,
        }, 200

    except (TypeError, ValueError) as exc:
        return {
            "error": str(exc)
        }, 400


@leads_bp.delete("/<int:lead_id>")
@jwt_required()
def delete(lead_id):
    deleted = remove_lead(lead_id)

    if not deleted:
        return {
            "error": "Lead not found"
        }, 404

    return {
        "message": "Lead deleted successfully"
    }, 200


@leads_bp.post("/<int:lead_id>/score")
@jwt_required()
def score_lead(lead_id):
    lead_obj = find_lead(lead_id)
    if not lead_obj:
        return {"error": "Lead not found"}, 404

    # Run ML prediction model
    from ai_ml_engine.inference.predict import predict_lead
    prediction = predict_lead({
        "account": lead_obj.get("company", "Default Account"),
        "sector": "technolgy",
        "sales_price": lead_obj.get("value", 50000.0),
    })

    # Update lead score in repository
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

