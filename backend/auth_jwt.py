from datetime import timedelta
from typing import Any

from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

try:
    from .database import User, get_session
except ImportError:
    from database import User, get_session


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
bcrypt = Bcrypt()


def _error(message: str, status_code: int):
    return jsonify({"success": False, "message": message}), status_code


@auth_bp.route("/register", methods=["POST"])
def register():
    data: dict[str, Any] = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not username or not email or not password:
        return _error("username, email, and password are required", 400)

    session = get_session()
    try:
        existing_user = session.query(User).filter(or_(User.username == username, User.email == email)).first()
        if existing_user:
            return _error("username or email already exists", 409)

        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(username=username, email=email, password_hash=password_hash)
        session.add(user)
        session.commit()
        return jsonify({"success": True, "message": "user registered", "data": user.to_dict()}), 201
    except IntegrityError:
        session.rollback()
        return _error("username or email already exists", 409)
    finally:
        session.close()


@auth_bp.route("/login", methods=["POST"])
def login():
    data: dict[str, Any] = request.get_json(silent=True) or {}
    identifier = (
        (data.get("username_or_email") or "").strip()
        or (data.get("email") or "").strip()
        or (data.get("username") or "").strip()
    )
    password = data.get("password") or ""

    if not identifier or not password:
        return _error("login identifier and password are required", 400)

    session = get_session()
    try:
        user = session.query(User).filter(or_(User.username == identifier, User.email == identifier.lower())).first()
        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            return _error("invalid credentials", 401)

        token = create_access_token(
            identity=str(user.id),
            additional_claims={"username": user.username},
            expires_delta=timedelta(hours=1),
        )
        return jsonify({"success": True, "message": "login successful", "data": {"access_token": token}}), 200
    finally:
        session.close()


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    session = get_session()
    try:
        user = session.get(User, int(user_id))
        if not user:
            return _error("user not found", 404)
        return jsonify({"success": True, "data": user.to_dict()}), 200
    finally:
        session.close()