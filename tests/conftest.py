import pytest
from werkzeug.security import generate_password_hash
from backend.app import create_app
from backend.app.extensions import db
from backend.app.models import User

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()
        # Seed test admin user
        user = User(
            name="Test Rep",
            email="testrep@salesgenie.ai",
            password_hash=generate_password_hash("Password123!"),
            role="sales_rep",
        )
        db.session.add(user)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    res = client.post("/api/auth/register", json={
        "name": "Auth User",
        "email": "authuser@salesgenie.ai",
        "password": "Password123!",
        "confirm_password": "Password123!"
    })
    token = None
    if res.status_code == 201:
        login_res = client.post("/api/auth/login", json={
            "email": "authuser@salesgenie.ai",
            "password": "Password123!"
        })
        token = login_res.json.get("access_token")
    else:
        login_res = client.post("/api/auth/login", json={
            "email": "authuser@salesgenie.ai",
            "password": "Password123!"
        })
        token = login_res.json.get("access_token")
    return {"Authorization": f"Bearer {token}"}

