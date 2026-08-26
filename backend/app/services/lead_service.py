from ..repositories.lead_repository import (
    create_lead,
    delete_lead,
    get_all_leads,
    get_lead_by_id,
    update_lead,
)


def serialize_lead(lead):
    return {
        "id": lead.id,
        "company": lead.company,
        "contact_name": lead.contact_name,
        "email": lead.email,
        "phone": lead.phone,
        "stage": lead.stage,
        "status": lead.status,
        "value": lead.value,
        "lead_score": lead.lead_score,
        "purchase_probability": lead.purchase_probability,
        "last_contact_at": (
            lead.last_contact_at.isoformat()
            if lead.last_contact_at
            else None
        ),
        "response_time": lead.response_time,
        "sales_cycle": lead.sales_cycle,
        "assigned_to": lead.assigned_to,
        "created_at": (
            lead.created_at.isoformat()
            if lead.created_at
            else None
        ),
        "updated_at": (
            lead.updated_at.isoformat()
            if lead.updated_at
            else None
        ),
    }


def list_leads():
    return [serialize_lead(lead) for lead in get_all_leads()]


def find_lead(lead_id):
    lead = get_lead_by_id(lead_id)

    if not lead:
        return None

    return serialize_lead(lead)


def add_lead(data):
    lead = create_lead(data)
    return serialize_lead(lead)


def edit_lead(lead_id, data):
    lead = get_lead_by_id(lead_id)

    if not lead:
        return None

    lead = update_lead(lead, data)

    return serialize_lead(lead)


def remove_lead(lead_id):
    lead = get_lead_by_id(lead_id)

    if not lead:
        return False

    delete_lead(lead)

    return True
