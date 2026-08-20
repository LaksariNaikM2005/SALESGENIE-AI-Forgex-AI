import os
import sys

# Ensure parent directory and workspace root are in path for absolute imports of siblings
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request, g
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity

# 1. Import your database and security extensions
from database import db
from utils.security import bcrypt

# 2. Import your API Blueprints
from routes.lead_routes import lead_bp
from routes.kpi_routes import kpi_bp
from routes.auth_routes import auth_bp

try:
    from automation.api.crm_endpoints import automation_bp
except ImportError:
    from api.crm_endpoints import automation_bp

try:
    from ml_engine.lead_scoring import train_and_predict_lead
except ImportError:
    from lead_scoring import train_and_predict_lead

app = Flask(__name__)

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
    app.run(debug=True, port=5000)