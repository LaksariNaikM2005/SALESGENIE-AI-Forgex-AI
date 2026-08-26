from datetime import datetime, timezone

from ..extensions import db


class AIRecommendation(db.Model):
    __tablename__ = "ai_recommendations"

    id = db.Column(db.Integer, primary_key=True)

    lead_id = db.Column(
        db.Integer,
        db.ForeignKey("leads.id"),
        nullable=False,
        index=True,
    )

    recommendation = db.Column(
        db.Text,
        nullable=False,
    )

    priority = db.Column(
        db.String(50),
        nullable=False,
        default="Medium",
    )

    reason = db.Column(
        db.Text,
        nullable=True,
    )

    completed = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    generated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    lead = db.relationship(
        "Lead",
        back_populates="recommendations",
    )