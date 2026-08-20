from flask import Blueprint, jsonify, request

feature_bp = Blueprint('feature_bp', __name__)

@feature_bp.route('/company-details/<int:id>', methods=['GET'])
def get_company_details(id):
    # Placeholder for Sales Intelligence data
    return jsonify({"company_id": id, "intel": "Recent funding round raised $5M."}), 200

@feature_bp.route('/ai-lead-intelligence/<int:id>', methods=['GET'])
def get_ai_intelligence(id):
    return jsonify({"lead_id": id, "insights": ["High intent to buy", "Decision maker"]}), 200

@feature_bp.route('/outreach', methods=['POST'])
def generate_outreach():
    data = request.json
    # Placeholder for Member 2's AI email generation
    email_body = f"Hello {data.get('name', 'there')}, we noticed your company is growing..."
    return jsonify({"generated_email": email_body}), 200

@feature_bp.route('/conversation-intelligence', methods=['POST'])
def analyze_conversation():
    # Placeholder for meeting transcript analysis
    return jsonify({"summary": "Client requested a demo next week.", "sentiment": "Positive"}), 200

@feature_bp.route('/meetings', methods=['GET'])
def get_meetings():
    return jsonify([{"id": 1, "time": "2026-08-21T10:00:00", "status": "Scheduled"}]), 200

@feature_bp.route('/follow-ups', methods=['GET'])
def get_follow_ups():
    return jsonify([{"lead_id": 12, "action": "Send follow-up email", "due": "Today"}]), 200

@feature_bp.route('/notifications', methods=['GET'])
def get_notifications():
    return jsonify([{"id": 1, "message": "Lead score for TechCorp increased to 95!"}]), 200

@feature_bp.route('/reports', methods=['GET'])
def get_reports():
    return jsonify({"weekly_conversion": "12%", "revenue_forecast": "$150,000"}), 200