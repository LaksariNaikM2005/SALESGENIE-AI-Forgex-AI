import logging
from ..extensions import db
from ..models import AIRecommendation, Lead
from ai_ml_engine.inference.predict import predict_lead

logger = logging.getLogger(__name__)


def generate_ai_lead_insights(lead) -> dict:
    """
    Generates rich, dynamic AI lead intelligence, risk assessment, key drivers,
    pricing strategy, and next-best-action recommendations based on real ML predictions
    and lead metadata.
    """
    from .lead_service import build_ml_input, serialize_lead

    lead_dict = serialize_lead(lead)
    ml_input = build_ml_input(lead_dict)

    prediction = predict_lead(ml_input)
    score = prediction["lead_score"]
    prob = prediction["purchase_probability"]
    value = float(lead.value or 125000.0)

    stage = (lead.stage or "New Lead").lower()
    status = (lead.status or "Open").lower()
    company = lead.company or "Enterprise Prospect"

    drivers = []
    if value >= 200000.0:
        drivers.append("High deal value ($200k+) represents enterprise-tier revenue potential.")
    elif value >= 100000.0:
        drivers.append("Mid-tier capital expenditure deal aligned with manufacturing standards.")

    if prob >= 0.70 or score >= 70.0:
        drivers.append("Strong historical win rate signals across sales agent and product series.")
        priority = "High"
        risk_level = "Low"
        action = f"Schedule executive SLA agreement & plant tour with {lead.contact_name or 'decision maker'}."
        pricing_strategy = "Standard enterprise pricing (0-5% max discount incentive)."
        reason = f"High ML conversion score ({score}/100) indicates strong purchasing intent."
    elif prob >= 0.40 or score >= 40.0:
        drivers.append("Moderate account engagement and historical sector stability.")
        priority = "Medium"
        risk_level = "Medium"
        action = f"Deliver technical engineering ROI demo & equipment specs to {company}."
        pricing_strategy = "Offer 5-8% volume incentive discount if closed within current quarter."
        reason = f"Moderate conversion probability ({round(prob * 100, 1)}%). Technical briefing required."
    else:
        drivers.append("Long sales cycle or lower historical conversion rate in this vertical.")
        priority = "Low"
        risk_level = "High"
        action = f"Send automated technical case study & schedule quarterly follow-up call."
        pricing_strategy = "Require standard deposit terms with pilot evaluation option."
        reason = f"Lower ML qualification score ({score}/100). Nurture prospect with technical whitepapers."

    if "qualified" in stage:
        action = f"Present formal proposal and technical SCADA/PLC integration roadmap to {company}."
        priority = "High"
    elif "proposal" in stage:
        action = f"Follow up on executive proposal approval with {lead.contact_name or 'Head of Operations'}."
        priority = "High"
    elif "negotiation" in stage:
        action = f"Finalize contract terms and warranty service agreement for {company}."
        priority = "High"

    return {
        "lead_id": lead.id,
        "company": company,
        "lead_score": score,
        "purchase_probability": prob,
        "prediction": prediction["prediction"],
        "priority": priority,
        "risk_level": risk_level,
        "key_drivers": drivers,
        "recommendation": action,
        "pricing_strategy": pricing_strategy,
        "reason": reason,
    }


def create_recommendation(lead_id: int) -> AIRecommendation:
    """
    Generates and persists a dynamic AI recommendation for a lead.
    """
    lead = db.session.get(Lead, lead_id)
    if lead is None:
        return None

    insights = generate_ai_lead_insights(lead)

    # Check for existing pending recommendation
    rec = AIRecommendation.query.filter_by(lead_id=lead.id, completed=False).first()
    if not rec:
        rec = AIRecommendation(lead_id=lead.id)

    rec.recommendation = insights["recommendation"]
    rec.priority = insights["priority"]
    rec.reason = insights["reason"]

    db.session.add(rec)
    db.session.commit()
    return rec


def generate_all_recommendations() -> list[AIRecommendation]:
    """
    Scans all leads and generates/refreshes AI recommendations for every prospect.
    """
    leads = Lead.query.all()
    created = []
    for lead in leads:
        rec = create_recommendation(lead.id)
        if rec:
            created.append(rec)
    return created


def get_recommendations(lead_id: int):
    return (
        AIRecommendation.query.filter_by(lead_id=lead_id)
        .order_by(AIRecommendation.generated_at.desc())
        .all()
    )


def update_recommendation(recommendation_id: int, data: dict):
    recommendation = db.session.get(AIRecommendation, recommendation_id)
    if recommendation is None:
        return None

    for field in ["recommendation", "priority", "reason", "completed"]:
        if field in data:
            setattr(recommendation, field, data[field])

    db.session.commit()
    return recommendation


def delete_recommendation(recommendation_id: int) -> bool:
    recommendation = db.session.get(AIRecommendation, recommendation_id)
    if recommendation is None:
        return False

    db.session.delete(recommendation)
    db.session.commit()
    return True