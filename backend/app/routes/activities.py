from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..extensions import db
from ..models.lead import Lead
from ..models.lead_activity import LeadActivity


activities_bp = Blueprint(
    "activities",
    __name__,
    url_prefix="/api/leads",
)


@activities_bp.post("/<int:lead_id>/activities")
@jwt_required()
def create_activity(lead_id):
    lead = db.session.get(Lead, lead_id)

    if not lead:
        return jsonify({
            "message": "Lead not found"
        }), 404

    data = request.get_json() or {}

    activity_type = data.get("activity_type")
    description = data.get("description")

    if not activity_type:
        return jsonify({
            "message": "activity_type is required"
        }), 400

    activity = LeadActivity(
        lead_id=lead_id,
        activity_type=activity_type,
        description=description,
    )

    db.session.add(activity)
    db.session.commit()

    return jsonify({
        "message": "Activity created successfully",
        "activity": {
            "id": activity.id,
            "lead_id": activity.lead_id,
            "activity_type": activity.activity_type,
            "description": activity.description,
            "activity_at": activity.activity_at.isoformat(),
            "created_at": activity.created_at.isoformat(),
        },
    }), 201


@activities_bp.get("/<int:lead_id>/activities")
@jwt_required()
def get_activities(lead_id):
    lead = db.session.get(Lead, lead_id)

    if not lead:
        return jsonify({
            "message": "Lead not found"
        }), 404

    activities = (
        LeadActivity.query
        .filter_by(lead_id=lead_id)
        .order_by(LeadActivity.activity_at.desc())
        .all()
    )

    return jsonify({
        "activities": [
            {
                "id": activity.id,
                "lead_id": activity.lead_id,
                "activity_type": activity.activity_type,
                "description": activity.description,
                "activity_at": activity.activity_at.isoformat(),
                "created_at": activity.created_at.isoformat(),
            }
            for activity in activities
        ]
    }), 200