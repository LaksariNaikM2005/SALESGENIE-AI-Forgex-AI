from ..extensions import db
from ..models import Lead


def get_all_leads():
    return Lead.query.order_by(Lead.created_at.desc()).all()


def get_lead_by_id(lead_id):
    return db.session.get(Lead, lead_id)


def create_lead(data):
    lead = Lead(
        company=data["company"],
        contact_name=data.get("contact_name"),
        email=data.get("email"),
        phone=data.get("phone"),
        stage=data.get("stage", "New Lead"),
        status=data.get("status", "Open"),
        value=float(data.get("value", 0)),
        lead_score=data.get("lead_score"),
        purchase_probability=data.get("purchase_probability"),
        response_time=data.get("response_time"),
        sales_cycle=data.get("sales_cycle"),
        assigned_to=data.get("assigned_to"),
    )

    db.session.add(lead)
    db.session.commit()

    return lead


def update_lead(lead, data):
    allowed_fields = [
        "company",
        "contact_name",
        "email",
        "phone",
        "stage",
        "status",
        "value",
        "lead_score",
        "purchase_probability",
        "response_time",
        "sales_cycle",
        "assigned_to",
    ]

    for field in allowed_fields:
        if field in data:
            setattr(lead, field, data[field])

    db.session.commit()

    return lead


def delete_lead(lead):
    db.session.delete(lead)
    db.session.commit()
