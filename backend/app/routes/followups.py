from datetime import datetime, timezone
import logging

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..extensions import db
from ..models.lead import Lead
from ..models.follow_up_history import FollowUpHistory
from ..models.ai_recommendation import AIRecommendation

logger = logging.getLogger(__name__)

followups_bp = Blueprint("followups", __name__)


def parse_datetime(value):
    """Convert an ISO datetime string into a Python datetime."""
    if not value:
        return None

    if isinstance(value, datetime):
        return value

    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))

        # Store timezone-aware values consistently.
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)

        return parsed
    except (TypeError, ValueError):
        return None


def get_next_best_action(lead: Lead) -> dict:
    """
    Derives AI Next-Best-Action for a follow-up task.
    Returns a dict with action, priority, reason, risk_level, pricing_strategy.
    """
    try:
        from ..services.ai_service import generate_ai_lead_insights
        insights = generate_ai_lead_insights(lead)
        return {
            "next_best_action": insights.get("recommendation", ""),
            "priority": insights.get("priority", "Medium"),
            "reason": insights.get("reason", ""),
            "risk_level": insights.get("risk_level", "Medium"),
            "pricing_strategy": insights.get("pricing_strategy", ""),
            "lead_score": insights.get("lead_score", 0),
            "purchase_probability": insights.get("purchase_probability", 0),
        }
    except Exception as e:
        logger.warning(f"Could not generate AI next-best-action for lead {lead.id}: {e}")
        return {
            "next_best_action": "Schedule a follow-up call to understand buyer needs.",
            "priority": "Medium",
            "reason": "AI insights unavailable - standard follow-up recommended.",
            "risk_level": "Medium",
            "pricing_strategy": "Standard pricing",
            "lead_score": None,
            "purchase_probability": None,
        }


def serialize_followup(followup, include_ai=True):
    """Convert FollowUpHistory model to API JSON with optional AI insights."""
    base = {
        "id": followup.id,
        "lead_id": followup.lead_id,
        "recommendation_id": followup.recommendation_id,
        "action": followup.action,
        "notes": followup.action,
        "status": followup.status,
        "scheduled_at": (
            followup.scheduled_at.isoformat()
            if followup.scheduled_at
            else None
        ),
        "follow_up_at": (
            followup.scheduled_at.isoformat()
            if followup.scheduled_at
            else None
        ),
        "completed_at": (
            followup.completed_at.isoformat()
            if followup.completed_at
            else None
        ),
        "created_at": (
            followup.created_at.isoformat()
            if followup.created_at
            else None
        ),
    }

    # Attach lead context
    if followup.lead:
        lead = followup.lead
        base["lead_company"] = lead.company
        base["lead_contact"] = lead.contact_name
        base["lead_stage"] = lead.stage
        base["lead_sector"] = lead.sector
        base["lead_value"] = lead.value
        base["lead_score"] = lead.lead_score
        base["purchase_probability"] = lead.purchase_probability

        if include_ai:
            ai_data = get_next_best_action(lead)
            base["ai"] = ai_data
    else:
        base["lead_company"] = None
        base["lead_contact"] = None
        base["lead_stage"] = None
        base["lead_sector"] = None
        base["lead_value"] = None
        base["lead_score"] = None
        base["purchase_probability"] = None
        base["ai"] = None

    return base



@followups_bp.route("/api/followups", methods=["GET"])
@jwt_required()
def get_all_global_followups():
    status = request.args.get("status")
    query = FollowUpHistory.query

    if status:
        query = query.filter_by(status=status)

    followups = query.order_by(FollowUpHistory.scheduled_at.desc()).all()

    return jsonify({
        "followups": [serialize_followup(f) for f in followups]
    }), 200


@followups_bp.route(
    "/api/leads/<int:lead_id>/followups",
    methods=["POST"]
)
@jwt_required()
def create_followup(lead_id):
    lead = db.session.get(Lead, lead_id)

    if not lead:
        return jsonify({"message": "Lead not found"}), 404

    data = request.get_json() or {}

    follow_up_at = data.get("follow_up_at")
    notes = data.get("notes")
    status = data.get("status", "pending")
    recommendation_id = data.get("recommendation_id")

    if not follow_up_at:
        return jsonify({
            "message": "follow_up_at is required"
        }), 400

    scheduled_at = parse_datetime(follow_up_at)

    if not scheduled_at:
        return jsonify({
            "message": "Invalid follow_up_at format. Use ISO 8601."
        }), 400

    allowed_statuses = {
        "pending",
        "completed",
        "cancelled",
    }

    if status not in allowed_statuses:
        return jsonify({
            "message": "Invalid status",
            "allowed_statuses": sorted(allowed_statuses),
        }), 400

    if not notes:
        return jsonify({
            "message": "notes is required"
        }), 400

    followup = FollowUpHistory(
        lead_id=lead_id,
        recommendation_id=recommendation_id,
        action=notes,
        status=status,
        scheduled_at=scheduled_at,
        completed_at=(
            datetime.now(timezone.utc)
            if status == "completed"
            else None
        ),
    )

    db.session.add(followup)
    db.session.commit()

    return jsonify({
        "message": "Follow-up created successfully",
        "followup": serialize_followup(followup),
    }), 201


@followups_bp.route(
    "/api/leads/<int:lead_id>/followups",
    methods=["GET"]
)
@jwt_required()
def get_followups(lead_id):
    lead = db.session.get(Lead, lead_id)

    if not lead:
        return jsonify({"message": "Lead not found"}), 404

    followups = (
        FollowUpHistory.query
        .filter_by(lead_id=lead_id)
        .order_by(FollowUpHistory.scheduled_at.asc())
        .all()
    )

    return jsonify({
        "followups": [
            serialize_followup(followup)
            for followup in followups
        ]
    }), 200


@followups_bp.route(
    "/api/followups/<int:followup_id>",
    methods=["PUT"]
)
@jwt_required()
def update_followup(followup_id):
    followup = db.session.get(FollowUpHistory, followup_id)

    if not followup:
        return jsonify({
            "message": "Follow-up not found"
        }), 404

    data = request.get_json() or {}

    if "follow_up_at" in data:
        scheduled_at = parse_datetime(data["follow_up_at"])

        if not scheduled_at:
            return jsonify({
                "message": "Invalid follow_up_at format. Use ISO 8601."
            }), 400

        followup.scheduled_at = scheduled_at

    if "notes" in data:
        if not data["notes"]:
            return jsonify({
                "message": "notes cannot be empty"
            }), 400

        followup.action = data["notes"]

    if "recommendation_id" in data:
        followup.recommendation_id = data["recommendation_id"]

    if "status" in data:
        allowed_statuses = {
            "pending",
            "completed",
            "cancelled",
        }

        if data["status"] not in allowed_statuses:
            return jsonify({
                "message": "Invalid status",
                "allowed_statuses": sorted(allowed_statuses),
            }), 400

        followup.status = data["status"]

        if data["status"] == "completed":
            if not followup.completed_at:
                followup.completed_at = datetime.now(timezone.utc)
        else:
            followup.completed_at = None

    db.session.commit()

    return jsonify({
        "message": "Follow-up updated successfully",
        "followup": serialize_followup(followup),
    }), 200


@followups_bp.route(
    "/api/followups/<int:followup_id>",
    methods=["DELETE"]
)
@jwt_required()
def delete_followup(followup_id):
    followup = db.session.get(FollowUpHistory, followup_id)

    if not followup:
        return jsonify({
            "message": "Follow-up not found"
        }), 404

    db.session.delete(followup)
    db.session.commit()

    return jsonify({
        "message": "Follow-up deleted successfully"
    }), 200