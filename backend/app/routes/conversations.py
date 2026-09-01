from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models import Lead, Conversation, ConversationInsight
from ..services.conversation_service import summarize_transcript

conversations_bp = Blueprint("conversations", __name__, url_prefix="/api/conversations")

@conversations_bp.post("/summarize")
@jwt_required()
def summarize_meeting():
    data = request.get_json() or {}
    lead_id = data.get("lead_id")
    transcript = data.get("transcript")

    if not transcript:
        return jsonify({"message": "Transcript is required"}), 400

    lead = db.session.get(Lead, lead_id) if lead_id else None

    # Call AI Conversation Intelligence Service
    analysis = summarize_transcript(transcript)

    conversation = Conversation(
        lead_id=lead.id if lead else None,
        title=data.get("title", f"Meeting on {analysis.get('meeting_date', 'Today')}"),
        transcript=transcript,
        summary=analysis.get("summary"),
        sentiment=analysis.get("sentiment"),
        sentiment_score=analysis.get("sentiment_score", 0.8),
    )
    db.session.add(conversation)
    db.session.flush()

    insights = []
    # Save Action Items
    for item in analysis.get("action_items", []):
        ci = ConversationInsight(conversation_id=conversation.id, insight_type="action_item", content=item)
        db.session.add(ci)
        insights.append({"type": "action_item", "content": item})

    # Save Budget Mentions
    for item in analysis.get("budget_mentions", []):
        ci = ConversationInsight(conversation_id=conversation.id, insight_type="budget_mention", content=item)
        db.session.add(ci)
        insights.append({"type": "budget_mention", "content": item})

    # Save Competitor Mentions
    for item in analysis.get("competitor_mentions", []):
        ci = ConversationInsight(conversation_id=conversation.id, insight_type="competitor_mention", content=item)
        db.session.add(ci)
        insights.append({"type": "competitor_mention", "content": item})

    db.session.commit()

    return jsonify({
        "id": conversation.id,
        "title": conversation.title,
        "summary": conversation.summary,
        "sentiment": conversation.sentiment,
        "sentiment_score": conversation.sentiment_score,
        "insights": insights,
        "customer_interest": analysis.get("customer_interest", "High"),
    }), 201

@conversations_bp.get("")
@jwt_required()
def get_conversations():
    lead_id = request.args.get("lead_id")
    query = Conversation.query
    if lead_id:
        query = query.filter_by(lead_id=lead_id)

    conversations = query.order_by(Conversation.created_at.desc()).all()
    return jsonify([
        {
            "id": c.id,
            "lead_id": c.lead_id,
            "title": c.title,
            "summary": c.summary,
            "sentiment": c.sentiment,
            "created_at": c.created_at.isoformat() if c.created_at else None,
            "insights_count": len(c.insights),
        } for c in conversations
    ]), 200
