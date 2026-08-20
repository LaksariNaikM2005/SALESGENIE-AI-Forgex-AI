import os
import sys
from datetime import datetime, timezone
from typing import Any

# Ensure parent directory and workspace root are in path for absolute imports of siblings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError

from database import init_db, get_session, close_session, Lead, User
from auth_jwt import auth_bp, bcrypt

try:
    from automation.api.crm_endpoints import automation_bp
except ImportError:
    from api.crm_endpoints import automation_bp

try:
    from ml_engine.lead_scoring import train_and_predict_lead
except ImportError:
    from lead_scoring import train_and_predict_lead

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)  # Enable Cross-Origin Resource Sharing

    # Configurations
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///" + os.path.join(basedir, "../../sales.db")
    )
    app.config["JWT_ALGORITHM"] = "RS256"
    private_key_path = os.path.join(basedir, "../private_key.pem")
    public_key_path = os.path.join(basedir, "../public_key.pem")
    with open(private_key_path, "r") as f:
        app.config["JWT_PRIVATE_KEY"] = f.read()
    with open(public_key_path, "r") as f:
        app.config["JWT_PUBLIC_KEY"] = f.read()

    # Initialize extensions
    bcrypt.init_app(app)
    JWTManager(app)
    init_db(app)

    # Teardown database sessions automatically
    app.teardown_appcontext(close_session)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth", name="auth_api")
    # Also register under legacy prefix to maintain complete compatibility
    app.register_blueprint(auth_bp, url_prefix="/auth", name="auth_legacy")
    app.register_blueprint(automation_bp)

    from flask import g
    from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

    @app.before_request
    def load_user():
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            if user_id:
                session = get_session()
                try:
                    g.current_user = session.get(User, int(user_id))
                finally:
                    session.close()
            else:
                g.current_user = None
        except Exception:
            g.current_user = None

    # API Routes
    @app.route("/api/leads", methods=["GET"])
    def get_leads():
        session = get_session()
        try:
            leads = session.query(Lead).order_by(Lead.id.desc()).all()
            return jsonify([lead.to_dict() for lead in leads]), 200
        except SQLAlchemyError as e:
            return jsonify({"success": False, "message": str(e)}), 500
        finally:
            session.close()

    @app.route("/api/leads", methods=["POST"])
    def add_lead():
        data: dict[str, Any] = request.get_json(silent=True) or {}
        company = (data.get("company") or "").strip()
        contact = (data.get("contact") or "").strip()
        designation = (data.get("designation") or "").strip()
        industry = (data.get("industry") or "").strip()
        stage = (data.get("stage") or "New Lead").strip()
        notes = (data.get("notes") or "").strip()

        if not company or not contact:
            return jsonify({"success": False, "message": "Company and main contact are required"}), 400

        try:
            revenue = float(data.get("revenue") or 0.0)
        except (TypeError, ValueError):
            revenue = 0.0

        try:
            score = float(data.get("score") or data.get("ai_score") or 0.0)
        except (TypeError, ValueError):
            score = 0.0

        # Calculate category based on score
        if score >= 70:
            category = "Hot"
        elif score >= 40:
            category = "Warm"
        else:
            category = "Cold"

        session = get_session()
        try:
            lead = Lead(
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
            session.add(lead)
            session.commit()
            return jsonify({"success": True, "message": "Lead added successfully", "data": lead.to_dict()}), 201
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({"success": False, "message": f"Database error: {str(e)}"}), 500
        finally:
            session.close()

    @app.route("/api/leads/<int:lead_id>", methods=["PUT"])
    def update_lead(lead_id: int):
        data: dict[str, Any] = request.get_json(silent=True) or {}
        session = get_session()
        try:
            lead = session.get(Lead, lead_id)
            if not lead:
                return jsonify({"success": False, "message": "Lead not found"}), 404

            # Update fields if provided
            if "company" in data:
                lead.company = data["company"].strip()
            if "contact" in data:
                lead.contact = data["contact"].strip()
            if "designation" in data:
                lead.designation = data["designation"].strip()
            if "industry" in data:
                lead.industry = data["industry"].strip()
            if "stage" in data:
                lead.stage = data["stage"].strip()
            if "notes" in data:
                lead.notes = data["notes"].strip()
            if "revenue" in data:
                try:
                    lead.revenue = float(data["revenue"])
                except (TypeError, ValueError):
                    pass
            if "score" in data or "ai_score" in data:
                try:
                    score = float(data.get("score") or data.get("ai_score") or 0.0)
                    lead.score = score
                    # Auto recalculate category
                    if score >= 70:
                        lead.category = "Hot"
                    elif score >= 40:
                        lead.category = "Warm"
                    else:
                        lead.category = "Cold"
                except (TypeError, ValueError):
                    pass

            session.commit()
            return jsonify({"success": True, "message": "Lead updated successfully", "data": lead.to_dict()}), 200
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({"success": False, "message": f"Database error: {str(e)}"}), 500
        finally:
            session.close()

    @app.route("/api/leads/<int:lead_id>", methods=["DELETE"])
    def delete_lead(lead_id: int):
        session = get_session()
        try:
            lead = session.get(Lead, lead_id)
            if not lead:
                return jsonify({"success": False, "message": "Lead not found"}), 404
            session.delete(lead)
            session.commit()
            return jsonify({"success": True, "message": "Lead deleted successfully"}), 200
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({"success": False, "message": f"Database error: {str(e)}"}), 500
        finally:
            session.close()

    @app.route("/api/kpis", methods=["GET"])
    def get_kpis():
        session = get_session()
        try:
            leads = session.query(Lead).all()
            total_leads = len(leads)
            won_leads = len([lead for lead in leads if lead.stage.lower() == "closed won"])
            
            conversion_rate = round((won_leads / total_leads * 100), 2) if total_leads else 0.0
            pipeline_value = round(sum((lead.revenue or 0.0) for lead in leads), 2)
            avg_score = round(sum((lead.score or 0.0) for lead in leads) / total_leads, 2) if total_leads else 0.0
            avg_cycle_days = 14.5 if total_leads else 0.0

            return jsonify({
                "success": True,
                "data": {
                    "total_leads": total_leads,
                    "conversion_rate": conversion_rate,
                    "pipeline_value": pipeline_value,
                    "average_score": avg_score,
                    "average_cycle_days": avg_cycle_days
                }
            }), 200
        except SQLAlchemyError as e:
            return jsonify({"success": False, "message": str(e)}), 500
        finally:
            session.close()

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

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)