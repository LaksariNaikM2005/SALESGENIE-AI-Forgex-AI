from datetime import datetime, timezone
from ..extensions import db

class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey("leads.id"), nullable=True, index=True)
    title = db.Column(db.String(255), nullable=True)
    transcript = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=True)
    sentiment = db.Column(db.String(50), nullable=True)  # Positive, Neutral, Negative
    sentiment_score = db.Column(db.Float, nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    lead = db.relationship("Lead", back_populates="conversations")
    insights = db.relationship("ConversationInsight", back_populates="conversation", cascade="all, delete-orphan")


class ConversationInsight(db.Model):
    __tablename__ = "conversation_insights"

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.id"), nullable=False, index=True)
    insight_type = db.Column(db.String(50), nullable=False) # action_item, budget_mention, competitor_mention, next_meeting
    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    conversation = db.relationship("Conversation", back_populates="insights")
