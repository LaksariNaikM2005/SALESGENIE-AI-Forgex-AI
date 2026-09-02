import pytest
from flask_jwt_extended import create_access_token

def test_auth_001_valid_registration(client):
    res = client.post("/api/auth/register", json={
        "name": "Alice Smith",
        "email": "alice.smith@example.com",
        "password": "Password123!",
        "confirm_password": "Password123!"
    })
    assert res.status_code == 201
    assert res.json["user"]["email"] == "alice.smith@example.com"
    assert "password_hash" not in res.json["user"]


def test_auth_002_duplicate_email(client):
    client.post("/api/auth/register", json={
        "name": "Dup User",
        "email": "dup@example.com",
        "password": "Password123!",
        "confirm_password": "Password123!"
    })
    res = client.post("/api/auth/register", json={
        "name": "Dup User Two",
        "email": "dup@example.com",
        "password": "Password123!",
        "confirm_password": "Password123!"
    })
    assert res.status_code == 409
    assert "already exists" in res.json["error"].lower()


def test_auth_003_invalid_email(client):
    res = client.post("/api/auth/register", json={
        "name": "Bad Email",
        "email": "not-an-email",
        "password": "Password123!",
        "confirm_password": "Password123!"
    })
    assert res.status_code == 400
    assert "invalid email" in res.json["error"].lower()


def test_auth_004_missing_name(client):
    res = client.post("/api/auth/register", json={
        "email": "noname@example.com",
        "password": "Password123!",
        "confirm_password": "Password123!"
    })
    assert res.status_code == 400


def test_auth_005_missing_password(client):
    res = client.post("/api/auth/register", json={
        "name": "No Password",
        "email": "nopass@example.com"
    })
    assert res.status_code == 400


def test_auth_006_password_mismatch(client):
    res = client.post("/api/auth/register", json={
        "name": "Mismatch User",
        "email": "mismatch@example.com",
        "password": "Password123!",
        "confirm_password": "DifferentPassword123!"
    })
    assert res.status_code == 400
    assert "do not match" in res.json["error"].lower()


def test_auth_007_weak_short_password(client):
    res = client.post("/api/auth/register", json={
        "name": "Short Pass",
        "email": "shortpass@example.com",
        "password": "123",
        "confirm_password": "123"
    })
    assert res.status_code == 400
    assert "8 characters" in res.json["error"].lower()


def test_auth_008_valid_login(client):
    client.post("/api/auth/register", json={
        "name": "Valid Login User",
        "email": "loginuser@example.com",
        "password": "Password123!",
        "confirm_password": "Password123!"
    })
    res = client.post("/api/auth/login", json={
        "email": "loginuser@example.com",
        "password": "Password123!"
    })
    assert res.status_code == 200
    assert "access_token" in res.json
    assert res.json["user"]["email"] == "loginuser@example.com"


def test_auth_009_invalid_password(client):
    client.post("/api/auth/register", json={
        "name": "Wrong Pass User",
        "email": "wrongpass@example.com",
        "password": "Password123!"
    })
    res = client.post("/api/auth/login", json={
        "email": "wrongpass@example.com",
        "password": "WrongPassword!"
    })
    assert res.status_code == 401
    assert "invalid" in res.json["error"].lower()


def test_auth_010_invalid_email(client):
    res = client.post("/api/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "Password123!"
    })
    assert res.status_code == 401


def test_auth_012_missing_credentials(client):
    res = client.post("/api/auth/login", json={})
    assert res.status_code == 400


def test_auth_013_authenticated_user_accesses_protected_endpoint(client):
    reg_res = client.post("/api/auth/register", json={
        "name": "Protected Access User",
        "email": "protected@example.com",
        "password": "Password123!"
    })
    user_id = reg_res.json["user"]["id"]
    token = create_access_token(identity=str(user_id))

    res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json["email"] == "protected@example.com"


def test_auth_014_unauthenticated_user_accesses_protected_endpoint(client):
    res = client.get("/api/auth/me")
    assert res.status_code in (401, 422)


def test_auth_015_logout(client):
    res = client.post("/api/auth/logout")
    assert res.status_code == 200


def test_auth_017_get_current_user_profile(client):
    reg_res = client.post("/api/auth/register", json={
        "name": "Profile User",
        "email": "profile@example.com",
        "password": "Password123!"
    })
    user_id = reg_res.json["user"]["id"]
    token = create_access_token(identity=str(user_id))

    res = client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json["name"] == "Profile User"


def test_auth_018_update_profile(client):
    reg_res = client.post("/api/auth/register", json={
        "name": "Old Name",
        "email": "oldemail@example.com",
        "password": "Password123!"
    })
    user_id = reg_res.json["user"]["id"]
    token = create_access_token(identity=str(user_id))

    res = client.put("/api/users/me", json={
        "name": "New Name",
        "email": "newemail@example.com"
    }, headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 200
    assert res.json["user"]["name"] == "New Name"
    assert res.json["user"]["email"] == "newemail@example.com"


def test_auth_020_change_password(client):
    reg_res = client.post("/api/auth/register", json={
        "name": "Password Changer",
        "email": "pwdchange@example.com",
        "password": "OldPassword123!"
    })
    user_id = reg_res.json["user"]["id"]
    token = create_access_token(identity=str(user_id))

    res = client.post("/api/auth/change-password", json={
        "current_password": "OldPassword123!",
        "new_password": "NewPassword123!",
        "confirm_password": "NewPassword123!"
    }, headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 200

    # Verify login with new password
    login_res = client.post("/api/auth/login", json={
        "email": "pwdchange@example.com",
        "password": "NewPassword123!"
    })
    assert login_res.status_code == 200


def test_auth_021_wrong_current_password(client):
    reg_res = client.post("/api/auth/register", json={
        "name": "Wrong Pwd User",
        "email": "wrongpwd@example.com",
        "password": "OriginalPassword123!"
    })
    user_id = reg_res.json["user"]["id"]
    token = create_access_token(identity=str(user_id))

    res = client.post("/api/auth/change-password", json={
        "current_password": "WrongPassword123!",
        "new_password": "NewPassword123!",
        "confirm_password": "NewPassword123!"
    }, headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 401
    assert "incorrect" in res.json["error"].lower()
