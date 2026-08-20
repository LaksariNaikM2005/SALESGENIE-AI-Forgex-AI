from flask import Blueprint, request, jsonify
from extensions import db
from models.lead import Lead

from ml_engine.core.lead_scoring import predict_score

# Inside your POST /leads route...
lead_payload = request.json
calculated_score = predict_score(lead_payload)

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
        ai_score=calculated_score
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


def get_lead_stage(score):
    if score >= 90:
        return "Hot"
    elif score >= 70:
        return "Qualified"
    elif score >= 50:
        return "Warm"
    else:
        return "Cold"