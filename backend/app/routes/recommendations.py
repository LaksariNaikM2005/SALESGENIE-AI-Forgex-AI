from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..extensions import db
from ..models import AIRecommendation, Lead
from ..services.ai_service import (
    create_recommendation,
    delete_recommendation,
    generate_ai_lead_insights,
    generate_all_recommendations,
    get_recommendations,
    update_recommendation,
)
from ..services.lead_service import auto_seed_leads_if_empty

recommendations_bp = Blueprint(
    "recommendations",
    __name__,
    url_prefix="/api",
)


def serialize_recommendation(recommendation: AIRecommendation) -> dict:
    lead = recommendation.lead
    return {
        "id": recommendation.id,
        "lead_id": recommendation.lead_id,
        "lead_company": lead.company if lead else "General Prospect",
        "lead_contact": lead.contact_name if lead else "Decision Maker",
        "sector": getattr(lead, "sector", None) if lead else "Industrial Automation",
        "lead_score": getattr(lead, "lead_score", 85.0) if lead else 85.0,
        "purchase_probability": getattr(lead, "purchase_probability", 0.75) if lead else 0.75,
        "stage": getattr(lead, "stage", "Qualified") if lead else "Qualified",
        "recommendation": recommendation.recommendation,
        "priority": recommendation.priority,
        "reason": recommendation.reason,
        "completed": recommendation.completed,
        "generated_at": (
            recommendation.generated_at.isoformat()
            if recommendation.generated_at
            else None
        ),
    }


@recommendations_bp.get("/recommendations")
@jwt_required()
def get_global_recommendations():
    # Ensure leads and recommendations exist in database
    auto_seed_leads_if_empty()

    priority = request.args.get("priority")
    query = AIRecommendation.query

    if priority and priority.lower() != "all":
        query = query.filter_by(priority=priority)

    recommendations = query.order_by(AIRecommendation.generated_at.desc()).all()

    if not recommendations:
        generate_all_recommendations()
        query = AIRecommendation.query
        if priority and priority.lower() != "all":
            query = query.filter_by(priority=priority)
        recommendations = query.order_by(AIRecommendation.generated_at.desc()).all()

    return jsonify({
        "recommendations": [serialize_recommendation(item) for item in recommendations]
    }), 200


@recommendations_bp.post("/recommendations/generate-all")
@jwt_required()
def generate_all_endpoint():
    auto_seed_leads_if_empty()
    created = generate_all_recommendations()
    return jsonify({
        "message": f"Successfully generated AI recommendations for {len(created)} leads.",
        "total": len(created),
    }), 200


@recommendations_bp.get("/leads/<int:lead_id>/insights")
@jwt_required()
def get_lead_insights(lead_id):
    lead = db.session.get(Lead, lead_id)
    if lead is None:
        return jsonify({"message": "Lead not found"}), 404

    insights = generate_ai_lead_insights(lead)
    return jsonify(insights), 200


@recommendations_bp.post("/leads/<int:lead_id>/recommendations")
@jwt_required()
def create(lead_id):
    lead = db.session.get(Lead, lead_id)
    if lead is None:
        return jsonify({"message": "Lead not found"}), 404

    recommendation = create_recommendation(lead_id)
    return jsonify({
        "message": "Recommendation generated successfully",
        "recommendation": serialize_recommendation(recommendation),
    }), 201


@recommendations_bp.get("/leads/<int:lead_id>/recommendations")
@jwt_required()
def get_all(lead_id):
    lead = db.session.get(Lead, lead_id)
    if lead is None:
        return jsonify({"message": "Lead not found"}), 404

    recommendations = get_recommendations(lead_id)
    return jsonify({
        "recommendations": [serialize_recommendation(item) for item in recommendations]
    }), 200


@recommendations_bp.put("/recommendations/<int:recommendation_id>")
@jwt_required()
def update(recommendation_id):
    data = request.get_json(silent=True) or {}
    recommendation = update_recommendation(recommendation_id, data)

    if recommendation is None:
        return jsonify({"message": "Recommendation not found"}), 404

    return jsonify({
        "message": "Recommendation updated successfully",
        "recommendation": serialize_recommendation(recommendation),
    }), 200


@recommendations_bp.delete("/recommendations/<int:recommendation_id>")
@jwt_required()
def delete(recommendation_id):
    deleted = delete_recommendation(recommendation_id)
    if not deleted:
        return jsonify({"message": "Recommendation not found"}), 404

    return jsonify({"message": "Recommendation deleted successfully"}), 200