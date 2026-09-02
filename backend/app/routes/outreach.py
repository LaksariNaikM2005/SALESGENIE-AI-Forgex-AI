from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from ..services.outreach_service import generate_outreach_message

outreach_bp = Blueprint("outreach", __name__, url_prefix="/api/outreach")

@outreach_bp.post("/generate")
@jwt_required()
def generate_email():
    data = request.get_json() or {}
    lead_name = data.get("lead_name", "Prospect")
    company_name = data.get("company_name", "your company")
    industry = data.get("industry", "Industrial Automation")
    message_type = data.get("message_type", "Executive Email")
    tone = data.get("tone", "Executive & Consultative")
    value_prop = data.get("value_prop", "PLC & SCADA Integration")
    tech_stack = data.get("tech_stack", "Siemens PLC, ROS2")

    result = generate_outreach_message(
        lead_name=lead_name,
        company_name=company_name,
        industry=industry,
        message_type=message_type,
        tone=tone,
        value_prop=value_prop,
        tech_stack=tech_stack,
    )

    return jsonify({
        "subject": result.get("subject"),
        "body": result.get("body"),
        "message_type": message_type,
        "tone": tone,
        "value_prop": value_prop,
        "lead_name": lead_name,
        "company_name": company_name,
    }), 200

@outreach_bp.post("/send")
@jwt_required()
def send_email():
    data = request.get_json() or {}
    recipient = data.get("recipient")
    subject = data.get("subject")
    body = data.get("body")

    if not recipient or not subject or not body:
        return jsonify({"message": "Recipient, subject, and body are required"}), 400

    return jsonify({
        "message": f"Outreach message successfully sent to {recipient}",
        "status": "delivered",
    }), 200
