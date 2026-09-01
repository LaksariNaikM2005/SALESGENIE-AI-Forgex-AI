from datetime import datetime, timezone
from ..extensions import db

class Contact(db.Model):
    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=True, index=True)
    name = db.Column(db.String(120), nullable=False)
    designation = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(255), nullable=True, index=True)
    phone = db.Column(db.String(50), nullable=True)
    is_decision_maker = db.Column(db.Boolean, nullable=False, default=False)
    decision_role = db.Column(db.String(100), nullable=True)  # e.g., "CTO", "Finance Manager"

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
    company_rel = db.relationship("Company", back_populates="contacts")
    leads = db.relationship("Lead", back_populates="contact_rel")
