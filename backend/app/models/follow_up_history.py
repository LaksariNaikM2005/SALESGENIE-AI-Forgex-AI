from datetime import datetime, timezone

from ..extensions import db


class FollowUpHistory(db.Model):
    __tablename__ = "follow_up_history"

    id = db.Column(db.Integer, primary_key=True)

    lead_id = db.Column(
        db.Integer,
        db.ForeignKey("leads.id"),
        nullable=False,
        index=True,
    )

    recommendation_id = db.Column(
        db.Integer,
        db.ForeignKey("ai_recommendations.id"),
        nullable=True,
        index=True,
    )

    action = db.Column(
        db.Text,
        nullable=False,
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="pending",
    )

    scheduled_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True,
    )

    completed_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    lead = db.relationship(
        "Lead",
        back_populates="follow_ups",
    )

    recommendation = db.relationship(
        "AIRecommendation",
    )