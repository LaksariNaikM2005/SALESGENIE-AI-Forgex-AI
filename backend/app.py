import os
import sys

# Ensure parent directory and workspace root are in path for absolute imports of siblings
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request, g, render_template, redirect, url_for
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity

# Import database and security extensions
from extensions import db
from utils.security import bcrypt

# Import API Blueprints
from routes.lead_routes import lead_bp
from routes.kpi_routes import kpi_bp
from routes.auth_routes import auth_bp
from routes.feature_routes import feature_bp
from models import User, Lead, FollowUp, Meeting, Activity, Notification, Email

try:
    from automation.api.crm_endpoints import automation_bp
except ImportError:
    from api.crm_endpoints import automation_bp

try:
    from ml_engine.lead_scoring import train_and_predict_lead
except ImportError:
    from lead_scoring import train_and_predict_lead

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static",
)

# 3. Configure your Database and JWT Security
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'sales.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'vtusalesgenie-secure-key-2026' # Keep this secure in production

# 4. Initialize the extensions with your Flask app
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

# 5. Register the Blueprints (This exposes your API routes)
app.register_blueprint(lead_bp, url_prefix='/api')
app.register_blueprint(kpi_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(automation_bp)
app.register_blueprint(feature_bp, url_prefix='/api')

@app.route("/")
def index():
    leads = Lead.query.order_by(Lead.id.desc()).all()
    total_leads = len(leads)
    won_leads = len([lead for lead in leads if lead.stage.lower() == "closed won"])
    conversion_rate = round((won_leads / total_leads * 100), 2) if total_leads else 0.0
    pipeline_value = round(sum((lead.revenue or 0.0) for lead in leads), 2)
    return render_template(
        "index.html",
        leads=leads,
        total_leads=total_leads,
        conversion_rate=conversion_rate,
        conversion=conversion_rate,
        pipeline_value=pipeline_value,
    )

@app.route("/add", methods=["GET", "POST"])
def add_lead():
    if request.method == "POST":
        company = request.form.get("company", "").strip()
        contact = request.form.get("contact", "").strip()
        designation = request.form.get("designation", "").strip()
        industry = request.form.get("industry", "").strip()
        stage = request.form.get("stage", "New Lead").strip()
        notes = request.form.get("notes", "").strip()
        
        try:
            revenue = float(request.form.get("revenue") or 0.0)
        except (ValueError, TypeError):
            revenue = 0.0
            
        try:
            score = float(request.form.get("score") or 0.0)
        except (ValueError, TypeError):
            score = 0.0
            
        if score >= 70:
            category = "Hot"
        elif score >= 40:
            category = "Warm"
        else:
            category = "Cold"
            
        new_lead = Lead(
            company=company,
            contact=contact,
            designation=designation,
            industry=industry,
            revenue=revenue,
            stage=stage,
            score=score,
            category=category,
            notes=notes
        )
        db.session.add(new_lead)
        db.session.commit()
        return redirect(url_for("index"))
        
    return render_template("add_lead.html")

@app.before_request
def load_user():
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
        if user_id:
            from models.user import User
            g.current_user = db.session.get(User, int(user_id))
        else:
            g.current_user = None
    except Exception:
        g.current_user = None

@app.route("/api/predict", methods=["POST"])
def predict():
    payload = request.get_json() or {}
    try:
        emails = int(payload.get("emails", 0))
        visits = int(payload.get("visits", 0))
        demo = 1 if payload.get("demo") else 0
        
        score = train_and_predict_lead(emails, visits, demo)
        
        # Determine category
        if score >= 70:
            category = "Hot"
        elif score >= 40:
            category = "Warm"
        else:
            category = "Cold"
            
        return jsonify({
            "success": True,
            "score": score,
            "category": category
        })
    except Exception as exc:
        return jsonify({"success": False, "message": str(exc)}), 500

# 6. Create the database tables if they don't exist
with app.app_context():
    db.create_all()
    print("Database tables initialized successfully.")

if __name__ == '__main__':
    print("Starting SalesGenie AI Backend Server...")
    app.run(debug=True, use_reloader=False, port=5000)