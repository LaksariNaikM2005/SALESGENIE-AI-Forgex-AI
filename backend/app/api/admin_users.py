from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .auth import require_admin
from ..core.security import hash_password
from ..database import get_db
from ..models.user import User
from ..schemas.user import AdminCreateUser, UserResponse

router = APIRouter(prefix="/api/admin/users", tags=["Admin Users"])

DbSession = Annotated[Session, Depends(get_db)]
AdminUser = Annotated[User, Depends(require_admin)]


@router.get("", response_model=list[UserResponse])
def list_users(db: DbSession, admin: AdminUser):
    return db.query(User).order_by(User.id.desc()).all()


@router.post("", response_model=UserResponse, status_code=201)
def create_user(
    data: AdminCreateUser,
    db: DbSession,
    admin: AdminUser,
):
    email = str(data.email).lower()

    if db.query(User).filter_by(email=email).first():
        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists",
        )

    user = User(
        name=data.name.strip(),
        email=email,
        password_hash=hash_password(data.password),
        role=data.role,
        is_active=True,
    )

    db.add(user)

    try:
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise

    # Never return password_hash.
    return user


@router.patch("/{user_id}/status", response_model=UserResponse)
def update_user_status(
    user_id: int,
    is_active: bool,
    db: DbSession,
    admin: AdminUser,
):
    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == admin.id and not is_active:
        raise HTTPException(
            status_code=400,
            detail="You cannot deactivate your own account",
        )

    if user.role == "admin" and user.is_active and not is_active:
        active_admins = db.query(User).filter_by(
            role="admin", is_active=True
        ).count()

        if active_admins <= 1:
            raise HTTPException(
                status_code=409,
                detail="Cannot deactivate the last active administrator",
            )

    user.is_active = is_active
    db.commit()
    db.refresh(user)
    return user