from flask import Blueprint, jsonify
from models.lead import Lead

kpi_bp = Blueprint('kpi_bp', __name__)

@kpi_bp.route('/kpis', methods=['GET'])
def get_kpis():
    leads = Lead.query.all()
    total_leads = len(leads)
    
    # Logic to calculate pipeline value and average score
    pipeline_value = total_leads * 15000  # Assuming $15k per lead for the demo
    avg_score = sum(l.ai_score for l in leads) / total_leads if total_leads > 0 else 0
    
    return jsonify({
        "total_leads": total_leads,
        "pipeline_value": pipeline_value,
        "avg_ai_score": round(avg_score, 1)
    }), 200