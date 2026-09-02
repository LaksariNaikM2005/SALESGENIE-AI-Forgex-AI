from datetime import datetime, timezone
import re
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..extensions import db
from ..models import User

users_bp = Blueprint("users", __name__, url_prefix="/api/users")
EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


@users_bp.get("/me")
@jwt_required()
def get_current_user_profile():
    user_id = get_jwt_identity()
    user = db.session.get(User, int(user_id))

    if not user:
        return {"error": "User not found"}, 404

    return user.to_dict(), 200


@users_bp.put("/me")
@jwt_required()
def update_current_user_profile():
    user_id = get_jwt_identity()
    user = db.session.get(User, int(user_id))

    if not user:
        return {"error": "User not found"}, 404

    data = request.get_json() or {}

    name = data.get("name")
    email = data.get("email")

    if name is not None:
        if not name.strip():
            return {"error": "Name cannot be empty"}, 400
        user.name = name.strip()

    if email is not None:
        email = email.strip().lower()
        if not EMAIL_REGEX.match(email):
            return {"error": "Invalid email address format"}, 400

        # Check if email taken by another user
        existing = User.query.filter(User.email == email, User.id != user.id).first()
        if existing:
            return {"error": "Email is already in use by another user"}, 409

        user.email = email

    user.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    return {
        "message": "Profile updated successfully",
        "user": user.to_dict(),
    }, 200
