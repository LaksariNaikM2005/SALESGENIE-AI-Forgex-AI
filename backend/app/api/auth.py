from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from ..database import get_db, settings
from ..models.user import User
from ..schemas.user import LoginRequest, RegisterRequest
from ..core.security import (
    ALGORITHM,
    create_access_token,
    hash_password,
    verify_password,
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
bearer = HTTPBearer(auto_error=False)

DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(
    db: DbSession,
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer),
    ],
) -> User:
    unauthorized = HTTPException(
        status_code=401,
        detail="Authentication required",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise unauthorized

    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret_key,
            algorithms=[ALGORITHM],
        )
        user_id = int(payload["sub"])
    except (InvalidTokenError, KeyError, TypeError, ValueError):
        raise unauthorized

    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise unauthorized

    return user


def require_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Administrator permission required",
        )
    return current_user


def require_manager_or_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.role not in ("admin", "sales_manager"):
        raise HTTPException(
            status_code=403,
            detail="Manager or Administrator permission required",
        )
    return current_user


@router.post("/register", status_code=201)
def register(data: RegisterRequest, db: DbSession):
    email = str(data.email).lower()

    if db.query(User).filter_by(email=email).first():
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(
        name=data.name.strip(),
        email=email,
        password_hash=hash_password(data.password),
        role="sales_rep",  # Never accept a public role from the client.
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Account created",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        },
    }


@router.post("/login")
def login(data: LoginRequest, db: DbSession):
    email = str(data.email).lower()
    user = db.query(User).filter_by(email=email).first()

    if (
        user is None
        or not verify_password(data.password, user.password_hash)
        or not user.is_active
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        },
    }


@router.get("/me")
def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active,
    }