from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from werkzeug.security import check_password_hash, generate_password_hash

from ..database import settings

ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    if not password or not hashed:
        return False
    try:
        # Standard bcrypt
        if hashed.startswith("$2b$") or hashed.startswith("$2a$") or hashed.startswith("$2y$"):
            return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
        # Werkzeug (scrypt or pbkdf2)
        if "scrypt:" in hashed or "pbkdf2:" in hashed:
            return check_password_hash(hashed, password)
        # Direct fallback
        return check_password_hash(hashed, password)
    except Exception as exc:
        print(f"[Security] Password verification error: {exc}")
        return False


def create_access_token(user_id: int) -> str:
    expires = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    return jwt.encode(
        {"sub": str(user_id), "exp": expires},
        settings.jwt_secret_key,
        algorithm=ALGORITHM,
    )