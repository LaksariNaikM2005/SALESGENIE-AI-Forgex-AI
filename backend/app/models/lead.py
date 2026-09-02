from datetime import datetime, timezone

from ..extensions import db


class Lead(db.Model):
    __tablename__ = "leads"

    id = db.Column(db.Integer, primary_key=True)

    company = db.Column(
        db.String(255),
        nullable=False,
        index=True,
    )

    contact_name = db.Column(
        db.String(120),
        nullable=True,
    )

    email = db.Column(
        db.String(255),
        nullable=True,
        index=True,
    )

    phone = db.Column(
        db.String(50),
        nullable=True,
    )

    stage = db.Column(
        db.String(50),
        nullable=False,
        default="New Lead",
        index=True,
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="Open",
        index=True,
    )

    value = db.Column(
        db.Float,
        nullable=False,
        default=0.0,
    )

    sector = db.Column(
        db.String(100),
        nullable=True,
        default="Industrial Automation",
        index=True,
    )

    product = db.Column(
        db.String(150),
        nullable=True,
        default="Robotic Assembly Cell X7",
    )

    tech_stack = db.Column(
        db.String(255),
        nullable=True,
        default="ROS2, Siemens PLC, Fanuc CNC",
    )

    revenue = db.Column(
        db.Float,
        nullable=True,
        default=85.0,
    )

    employees = db.Column(
        db.Integer,
        nullable=True,
        default=1450,
    )

    sales_agent = db.Column(
        db.String(120),
        nullable=True,
        default="Marcus Vance",
    )

    lead_score = db.Column(
        db.Float,
        nullable=True,
    )

    purchase_probability = db.Column(
        db.Float,
        nullable=True,
    )

    last_contact_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True,
    )

    response_time = db.Column(
        db.Float,
        nullable=True,
    )

    sales_cycle = db.Column(
        db.Float,
        nullable=True,
    )

    assigned_to = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

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

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("companies.id"),
        nullable=True,
        index=True,
    )

    contact_id = db.Column(
        db.Integer,
        db.ForeignKey("contacts.id"),
        nullable=True,
        index=True,
    )

    assigned_user = db.relationship(
        "User",
        back_populates="leads",
    )

    company_rel = db.relationship(
        "Company",
        back_populates="leads",
    )

    contact_rel = db.relationship(
        "Contact",
        back_populates="leads",
    )

    activities = db.relationship(
        "LeadActivity",
        back_populates="lead",
        cascade="all, delete-orphan",
    )

    recommendations = db.relationship(
        "AIRecommendation",
        back_populates="lead",
        cascade="all, delete-orphan",
    )

    follow_ups = db.relationship(
        "FollowUpHistory",
        back_populates="lead",
        cascade="all, delete-orphan",
    )

    opportunities = db.relationship(
        "Opportunity",
        back_populates="lead",
        cascade="all, delete-orphan",
    )

    conversations = db.relationship(
        "Conversation",
        back_populates="lead",
        cascade="all, delete-orphan",
    )