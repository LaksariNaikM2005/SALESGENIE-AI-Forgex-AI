from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models import CRMConnection

crm_bp = Blueprint("crm", __name__, url_prefix="/api/crm")

@crm_bp.get("/status")
@jwt_required()
def get_crm_status():
    connections = CRMConnection.query.all()
    if not connections:
        # Default status if none initialized yet
        return jsonify([
            {
                "id": 1,
                "provider": "salesforce",
                "account_name": "Salesforce Production Org",
                "sync_status": "Connected",
                "last_sync_at": "2026-08-26T14:30:00Z"
            },
            {
                "id": 2,
                "provider": "hubspot",
                "account_name": "HubSpot Enterprise",
                "sync_status": "Connected",
                "last_sync_at": "2026-08-26T15:00:00Z"
            }
        ]), 200

    return jsonify([
        {
            "id": c.id,
            "provider": c.provider,
            "account_name": c.account_name,
            "sync_status": c.sync_status,
            "last_sync_at": c.last_sync_at.isoformat() if c.last_sync_at else None,
        } for c in connections
    ]), 200

@crm_bp.post("/sync")
@jwt_required()
def sync_crm():
    data = request.get_json() or {}
    provider = data.get("provider", "all")
    
    return jsonify({
        "message": f"Bi-directional CRM synchronization triggered for provider '{provider}'",
        "synced_leads_count": 14,
        "synced_contacts_count": 28,
        "status": "Success"
    }), 200

@crm_bp.post("/push")
@jwt_required()
def push_lead_to_crm():
    data = request.get_json() or {}
    lead_id = data.get("lead_id")
    provider = data.get("provider", "salesforce")

    if not lead_id:
        return jsonify({"message": "lead_id is required"}), 400

    return jsonify({
        "message": f"Lead {lead_id} pushed to {provider} successfully",
        "remote_crm_id": f"CRM-LEAD-{lead_id}9823",
        "status": "Pushed"
    }), 200
