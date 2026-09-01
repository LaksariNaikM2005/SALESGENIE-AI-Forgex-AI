from datetime import datetime, timezone
from ..extensions import db

class Opportunity(db.Model):
    __tablename__ = "opportunities"

    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey("leads.id"), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    stage = db.Column(db.String(50), nullable=False, default="New Lead") # New Lead, Qualified, Proposal, Negotiation, Closed Won, Closed Lost
    amount = db.Column(db.Float, nullable=False, default=0.0)
    probability = db.Column(db.Float, nullable=False, default=0.2)
    expected_close_date = db.Column(db.DateTime(timezone=True), nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    lead = db.relationship("Lead", back_populates="opportunities")
