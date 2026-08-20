from flask import Blueprint, request, jsonify
from database import db
from models.lead import Lead

lead_bp = Blueprint('lead_bp', __name__)

@lead_bp.route('/leads', methods=['GET'])
def get_leads():
    leads = Lead.query.all()
    return jsonify([lead.to_dict() for lead in leads]), 200

@lead_bp.route('/leads', methods=['POST'])
def create_lead():
    data = request.json
    new_lead = Lead(
        company=data.get('company'),
        industry=data.get('industry', 'Unknown'),
        contact_person=data.get('contact_person', 'Unknown'),
        stage=data.get('stage', 'New Lead'),
        ai_score=data.get('score', 0)
    )
    db.session.add(new_lead)
    db.session.commit()
    return jsonify({"message": "Lead created successfully", "lead": new_lead.to_dict()}), 201

@lead_bp.route('/leads/<int:lead_id>', methods=['DELETE'])
def delete_lead(lead_id):
    lead = Lead.query.get(lead_id)
    if not lead:
        return jsonify({"error": "Lead not found"}), 404
    
    db.session.delete(lead)
    db.session.commit()
    return jsonify({"message": "Lead deleted successfully"}), 200