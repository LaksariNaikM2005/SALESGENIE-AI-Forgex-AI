def test_health_endpoint(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json["status"] == "ok"

def test_register_and_login_flow(client):
    reg_res = client.post("/api/auth/register", json={
        "name": "Jane Doe",
        "email": "janedoe@salesgenie.ai",
        "password": "SecurePassword123!"
    })
    assert reg_res.status_code == 201
    assert "user" in reg_res.json

    login_res = client.post("/api/auth/login", json={
        "email": "janedoe@salesgenie.ai",
        "password": "SecurePassword123!"
    })
    assert login_res.status_code == 200
    assert "access_token" in login_res.json

def test_protected_me_endpoint(client, auth_headers):
    res = client.get("/api/auth/me", headers=auth_headers)
    assert res.status_code == 200
    assert res.json["email"] == "authuser@salesgenie.ai"
