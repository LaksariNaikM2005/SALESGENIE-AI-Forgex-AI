from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..extensions import db
from ..models import User

def role_required(*allowed_roles):
    """
    Decorator enforcing Role-Based Access Control (RBAC).
    Admins are always authorized. Other roles must match allowed_roles.
    """
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = db.session.get(User, int(user_id))

            if not user:
                return jsonify({"error": "Unauthorized: User account not found"}), 401

            if not user.is_active:
                return jsonify({"error": "Forbidden: Account is inactive"}), 403

            # System Administrator role bypass
            if user.role == "admin":
                return fn(*args, **kwargs)

            # Check if user's role is allowed
            if user.role not in allowed_roles:
                return jsonify({
                    "error": f"Access Denied: Role '{user.role}' lacks permission for this operation.",
                    "required_roles": list(allowed_roles),
                }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
