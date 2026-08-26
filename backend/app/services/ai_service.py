from ..extensions import db
from ..models import AIRecommendation, Lead


def generate_recommendation(lead):
    """
    Generate a basic rule-based recommendation for a lead.
    This is the foundation for the future ML/AI recommendation engine.
    """

    score = lead.lead_score
    probability = lead.purchase_probability
    stage = (lead.stage or "").lower()
    status = (lead.status or "").lower()

    # High-priority lead
    if (
        (score is not None and score >= 80)
        or (probability is not None and probability >= 0.80)
    ):
        return {
            "recommendation": "Contact the lead immediately and prioritize follow-up.",
            "priority": "High",
            "reason": "The lead has a high score or high purchase probability.",
        }

    # Qualified lead
    if "qualified" in stage:
        return {
            "recommendation": "Schedule a product demonstration or sales meeting.",
            "priority": "High",
            "reason": "The lead has reached the qualified stage.",
        }

    # Closed leads
    if status in {"won", "closed"}:
        return {
            "recommendation": "Maintain the customer relationship and explore upselling opportunities.",
            "priority": "Low",
            "reason": "The lead has already been converted or closed.",
        }

    # Medium-priority lead
    if (
        (score is not None and score >= 50)
        or (probability is not None and probability >= 0.50)
    ):
        return {
            "recommendation": "Follow up with the lead and identify their current requirements.",
            "priority": "Medium",
            "reason": "The lead shows moderate conversion potential.",
        }

    # Default recommendation
    return {
        "recommendation": "Send an introductory message and collect more information about the lead.",
        "priority": "Medium",
        "reason": "Insufficient lead intelligence is available for a more specific recommendation.",
    }


def create_recommendation(lead_id):
    """
    Generate and save an AI recommendation for a lead.
    """

    lead = db.session.get(Lead, lead_id)

    if lead is None:
        return None

    result = generate_recommendation(lead)

    recommendation = AIRecommendation(
        lead_id=lead.id,
        recommendation=result["recommendation"],
        priority=result["priority"],
        reason=result["reason"],
    )

    db.session.add(recommendation)
    db.session.commit()

    return recommendation


def get_recommendations(lead_id):
    """
    Return all recommendations for a lead.
    """

    return (
        AIRecommendation.query
        .filter_by(lead_id=lead_id)
        .order_by(AIRecommendation.generated_at.desc())
        .all()
    )


def update_recommendation(recommendation_id, data):
    """
    Update an existing recommendation.
    """

    recommendation = db.session.get(
        AIRecommendation,
        recommendation_id,
    )

    if recommendation is None:
        return None

    allowed_fields = [
        "recommendation",
        "priority",
        "reason",
        "completed",
    ]

    for field in allowed_fields:
        if field in data:
            setattr(recommendation, field, data[field])

    db.session.commit()

    return recommendation


def delete_recommendation(recommendation_id):
    """
    Delete an existing recommendation.
    """

    recommendation = db.session.get(
        AIRecommendation,
        recommendation_id,
    )

    if recommendation is None:
        return False

    db.session.delete(recommendation)
    db.session.commit()

    return True