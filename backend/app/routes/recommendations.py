from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..models import Lead
from ..services.ai_service import (
    create_recommendation,
    get_recommendations,
    update_recommendation,
    delete_recommendation,
)
from ..extensions import db


recommendations_bp = Blueprint(
    "recommendations",
    __name__,
    url_prefix="/api",
)


def serialize_recommendation(recommendation):
    return {
        "id": recommendation.id,
        "lead_id": recommendation.lead_id,
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
        "recommendations": [
            serialize_recommendation(item)
            for item in recommendations
        ]
    }), 200


@recommendations_bp.put("/recommendations/<int:recommendation_id>")
@jwt_required()
def update(recommendation_id):
    data = request.get_json(silent=True) or {}

    recommendation = update_recommendation(
        recommendation_id,
        data,
    )

    if recommendation is None:
        return jsonify({
            "message": "Recommendation not found"
        }), 404

    return jsonify({
        "message": "Recommendation updated successfully",
        "recommendation": serialize_recommendation(recommendation),
    }), 200


@recommendations_bp.delete("/recommendations/<int:recommendation_id>")
@jwt_required()
def delete(recommendation_id):
    deleted = delete_recommendation(recommendation_id)

    if not deleted:
        return jsonify({
            "message": "Recommendation not found"
        }), 404

    return jsonify({
        "message": "Recommendation deleted successfully"
    }), 200