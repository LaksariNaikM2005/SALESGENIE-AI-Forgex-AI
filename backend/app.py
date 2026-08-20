import os
import sys
from typing import Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_jwt_extended import JWTManager
from sqlalchemy.exc import SQLAlchemyError

try:
    from .auth_jwt import auth_bp, bcrypt
    from .database import Lead, User, close_session, get_session, init_db
except ImportError:
    from auth_jwt import auth_bp, bcrypt
    from database import Lead, User, close_session, get_session, init_db

try:
    from automation.api.crm_endpoints import automation_bp
except ImportError:
    from api.crm_endpoints import automation_bp

try:
    from ml_engine.lead_scoring import train_and_predict_lead
except ImportError:
    from lead_scoring import train_and_predict_lead


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static",
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///sales.db")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-change-this-secret")

    bcrypt.init_app(app)
    JWTManager(app)
    init_db(app)
    app.teardown_appcontext(close_session)
    app.register_blueprint(auth_bp)
    app.register_blueprint(automation_bp)

    from flask import g
    from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

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

    @app.route("/")
    def index():
        session = get_session()
        try:
            leads = session.query(Lead).order_by(Lead.id.desc()).all()

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
        finally:
            session.close()

    @app.route("/add", methods=["GET", "POST"])
    def add_lead():
        if request.method == "GET":
            return render_template("add_lead.html")

        payload: dict[str, Any]
        if request.is_json:
            payload = request.get_json(silent=True) or {}
        else:
            payload = request.form.to_dict()
        company = (payload.get("company") or "").strip()
        contact = (payload.get("contact") or "").strip()
        designation = (payload.get("designation") or "").strip()
        industry = (payload.get("industry") or "").strip()
        stage = (payload.get("stage") or "New Lead").strip()
        notes = (payload.get("notes") or "").strip()

        if not company or not contact:
            error_response: dict[str, str | bool] = {
                "success": False,
                "message": "company and contact are required",
            }
            if request.is_json:
                return jsonify(error_response), 400
            return jsonify(error_response), 400

        try:
            revenue = float(payload.get("revenue") or 0)
        except (TypeError, ValueError):
            revenue = 0.0

        try:
            score = float(payload.get("score") or 0)
        except (TypeError, ValueError):
            score = 0.0

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
                notes=notes,
            )
            session.add(lead)
            session.commit()

            if request.is_json:
                return jsonify({"success": True, "data": lead.to_dict()}), 201
            return redirect(url_for("index"))
        except SQLAlchemyError:
            session.rollback()
            return jsonify({"success": False, "message": "failed to create lead"}), 500
        finally:
            session.close()

    @app.route("/delete/<int:lead_id>", methods=["POST", "DELETE"])
    def delete_lead(lead_id: int):
        session = get_session()
        try:
            lead = session.get(Lead, lead_id)
            if not lead:
                if request.is_json or request.method == "DELETE":
                    return jsonify({"success": False, "message": "lead not found"}), 404
                return redirect(url_for("index"))

            session.delete(lead)
            session.commit()

            if request.is_json or request.method == "DELETE":
                return jsonify({"success": True, "message": "lead deleted"}), 200
            return redirect(url_for("index"))
        except SQLAlchemyError:
            session.rollback()
            return jsonify({"success": False, "message": "failed to delete lead"}), 500
        finally:
            session.close()

    VALID_STAGES = ["New Lead", "Qualified", "Proposal", "Negotiation", "Closed Won"]

    @app.route("/update_stage/<int:lead_id>", methods=["POST", "PUT"])
    def update_stage(lead_id: int):
        payload: dict[str, Any]
        if request.is_json:
            payload = request.get_json(silent=True) or {}
        else:
            payload = request.form.to_dict()
        
        stage = (payload.get("stage") or "").strip()
        if not stage:
            return jsonify({"success": False, "message": "stage is required"}), 400

        # Normalize stage casing matching validation list
        matching_stages = [s for s in VALID_STAGES if s.lower() == stage.lower()]
        if not matching_stages:
            return jsonify({"success": False, "message": f"invalid stage. Must be one of: {', '.join(VALID_STAGES)}"}), 400
        validated_stage = matching_stages[0]

        session = get_session()
        try:
            lead = session.get(Lead, lead_id)
            if not lead:
                return jsonify({"success": False, "message": "lead not found"}), 404

            lead.stage = validated_stage
            session.commit()

            if request.is_json:
                return jsonify({"success": True, "data": lead.to_dict()}), 200
            return redirect(url_for("index"))
        except SQLAlchemyError:
            session.rollback()
            return jsonify({"success": False, "message": "failed to update stage"}), 500
        finally:
            session.close()

    @app.route("/update_score/<int:lead_id>", methods=["POST", "PUT"])
    def update_score(lead_id: int):
        payload: dict[str, Any]
        if request.is_json:
            payload = request.get_json(silent=True) or {}
        else:
            payload = request.form.to_dict()

        try:
            score = float(payload.get("score") or 0)
        except (TypeError, ValueError):
            return jsonify({"success": False, "message": "invalid score numeric value"}), 400

        # Determine categorization category
        if score >= 70:
            category = "Hot"
        elif score >= 40:
            category = "Warm"
        else:
            category = "Cold"

        session = get_session()
        try:
            lead = session.get(Lead, lead_id)
            if not lead:
                return jsonify({"success": False, "message": "lead not found"}), 404

            lead.score = score
            lead.category = category
            session.commit()

            return jsonify({"success": True, "data": lead.to_dict()}), 200
        except SQLAlchemyError:
            session.rollback()
            return jsonify({"success": False, "message": "failed to update score"}), 500
        finally:
            session.close()

    @app.route("/api/kpis", methods=["GET"])
    def api_kpis():
        session = get_session()
        try:
            leads = session.query(Lead).all()
            total_leads = len(leads)
            won_leads = len([lead for lead in leads if lead.stage.lower() == "closed won"])
            
            conversion_rate = round((won_leads / total_leads * 100), 2) if total_leads else 0.0
            pipeline_value = round(sum((lead.revenue or 0.0) for lead in leads), 2)
            avg_score = round(sum((lead.score or 0.0) for lead in leads) / total_leads, 2) if total_leads else 0.0
            
            # Simulated Response / Cycle metrics
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