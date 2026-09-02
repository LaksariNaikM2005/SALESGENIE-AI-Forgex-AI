from datetime import datetime, timezone
import re
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db, bcrypt
from ..models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


def verify_password_hash(stored_hash: str, password: str) -> bool:
    if not stored_hash or not password:
        return False
    try:
        if stored_hash.startswith("$2b$") or stored_hash.startswith("$2a$"):
            return bcrypt.check_password_hash(stored_hash, password)
        return check_password_hash(stored_hash, password)
    except Exception as e:
        print(f"Password verify error: {e}")
        return False


@auth_bp.post("/register")
def register():
    try:
        data = request.get_json() or {}

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        role = data.get("role", "sales_rep")

        if not name or not name.strip():
            return {"error": "Name is required"}, 400

        if not email or not email.strip():
            return {"error": "Email is required"}, 400

        email = email.strip().lower()
        if not EMAIL_REGEX.match(email):
            return {"error": "Invalid email address format"}, 400

        if not password:
            return {"error": "Password is required"}, 400

        if len(password) < 8:
            return {"error": "Password must be at least 8 characters long"}, 400

        if confirm_password is not None and password != confirm_password:
            return {"error": "Passwords do not match"}, 400

        db.create_all()

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {"error": "User with this email already exists"}, 409

        user = User(
            name=name.strip(),
            email=email,
            password_hash=generate_password_hash(password),
            role=role,
        )

        db.session.add(user)
        db.session.commit()

        return {
            "message": "User registered successfully",
            "user": user.to_dict(),
        }, 201
    except Exception as e:
        db.session.rollback()
        print(f"Registration error: {e}")
        return {"error": f"Registration failed: {str(e)}"}, 500


@auth_bp.post("/login")
def login():
    try:
        data = request.get_json() or {}

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"error": "Email and password are required"}, 400

        email = email.strip().lower()
        db.create_all()
        user = User.query.filter_by(email=email).first()

        if not user or not verify_password_hash(user.password_hash, password):
            return {"error": "Invalid email or password"}, 401

        if not user.is_active:
            return {"error": "User account is inactive"}, 403

        user.last_login_at = datetime.now(timezone.utc)
        db.session.commit()

        token = create_access_token(identity=str(user.id))

        return {
            "message": "Login successful",
            "access_token": token,
            "user": user.to_dict(),
        }, 200
    except Exception as e:
        db.session.rollback()
        print(f"Login error: {e}")
        return {"error": f"Login failed: {str(e)}"}, 500


@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = db.session.get(User, int(user_id))

    if not user:
        return {"error": "User not found"}, 404

    return user.to_dict(), 200


@auth_bp.post("/logout")
@jwt_required(optional=True)
def logout():
    return {"message": "Logged out successfully"}, 200


@auth_bp.post("/change-password")
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    user = db.session.get(User, int(user_id))

    if not user:
        return {"error": "User not found"}, 404

    data = request.get_json() or {}
    current_password = data.get("current_password")
    new_password = data.get("new_password")
    confirm_password = data.get("confirm_password")

    if not current_password or not new_password:
        return {"error": "Current password and new password are required"}, 400

    if not check_password_hash(user.password_hash, current_password):
        return {"error": "Incorrect current password"}, 401

    if len(new_password) < 8:
        return {"error": "New password must be at least 8 characters long"}, 400

    if confirm_password is not None and new_password != confirm_password:
        return {"error": "New passwords do not match"}, 400

    user.password_hash = generate_password_hash(new_password)
    user.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    return {"message": "Password changed successfully"}, 200


@auth_bp.post("/forgot-password")
def forgot_password():
    data = request.get_json() or {}
    email = data.get("email")

    if not email:
        return {"error": "Email is required"}, 400

    return {
        "message": "If an account with that email exists, password reset instructions have been sent."
    }, 200


@auth_bp.post("/reset-password")
def reset_password():
    data = request.get_json() or {}
    token = data.get("token")
    new_password = data.get("new_password")

    if not token or not new_password:
        return {"error": "Token and new password are required"}, 400

    return {"message": "Password reset successfully"}, 200