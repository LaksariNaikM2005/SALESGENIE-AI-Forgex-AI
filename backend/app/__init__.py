from flask import Flask

from .config import Config
from .extensions import bcrypt, cors, db, jwt, migrate


def create_app(config_class=Config):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Configure CORS
    cors.init_app(
        app,
        resources={
            r"/*": {
                "origins": "*"
            }
        },
    )

    # Import models
    from .models import (
        User,
        Lead,
        LeadActivity,
        AIRecommendation,
        FollowUpHistory,
        Company,
        Contact,
        Opportunity,
        Conversation,
        ConversationInsight,
        CRMConnection,
    )

    with app.app_context():
        try:
            db.create_all()
        except Exception:
            pass

    # Import route blueprints
    from .routes.auth import auth_bp
    from .routes.users import users_bp
    from .routes.leads import leads_bp
    from .routes.activities import activities_bp
    from .routes.recommendations import recommendations_bp
    from .routes.followups import followups_bp
    from .routes.ml import ml_bp
    from .routes.companies import companies_bp
    from .routes.contacts import contacts_bp
    from .routes.conversations import conversations_bp
    from .routes.outreach import outreach_bp
    from .routes.crm import crm_bp
    from .routes.analytics import analytics_bp

    # Register route blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(leads_bp)
    app.register_blueprint(activities_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(followups_bp)
    app.register_blueprint(ml_bp)
    app.register_blueprint(companies_bp)
    app.register_blueprint(contacts_bp)
    app.register_blueprint(conversations_bp)
    app.register_blueprint(outreach_bp)
    app.register_blueprint(crm_bp)
    app.register_blueprint(analytics_bp)

    # Root route
    @app.get("/")
    def index():
        return {
            "service": app.config["APP_NAME"],
            "status": "ok",
            "message": "SalesGenie AI Backend API Server Running",
            "health_check": "/api/health",
        }, 200

    # Health check
    @app.get("/api/health")
    def health():
        return {
            "status": "ok",
            "service": app.config["APP_NAME"],
        }, 200

    return app