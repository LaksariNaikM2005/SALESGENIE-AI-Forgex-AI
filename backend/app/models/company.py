from datetime import datetime, timezone
from ..extensions import db

class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    industry = db.Column(db.String(120), nullable=True, index=True)
    size = db.Column(db.String(50), nullable=True)  # e.g., "10-50", "500-1000"
    annual_revenue = db.Column(db.Float, nullable=True)
    location = db.Column(db.String(255), nullable=True)
    employee_count = db.Column(db.Integer, nullable=True)
    website = db.Column(db.String(255), nullable=True)
    technology_stack = db.Column(db.Text, nullable=True)  # Comma-separated or JSON string
    products_services = db.Column(db.Text, nullable=True)
    funding = db.Column(db.String(100), nullable=True)

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
    contacts = db.relationship("Contact", back_populates="company_rel", cascade="all, delete-orphan")
    leads = db.relationship("Lead", back_populates="company_rel")
