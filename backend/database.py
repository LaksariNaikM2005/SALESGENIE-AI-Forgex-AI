from datetime import datetime, timezone
from typing import Any

from flask import Flask
from sqlalchemy import DateTime, Float, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, scoped_session, sessionmaker

try:
    from extensions import db
except ImportError:
    from backend.extensions import db

from backend.models import User, Lead, FollowUp, Meeting, Activity, Notification, Email


SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False))
_engine = None


def init_db(app: Flask) -> None:
    global _engine

    db_uri = str(app.config.get("SQLALCHEMY_DATABASE_URI") or app.config.get("DATABASE_URL") or "sqlite:///sales.db")
    connect_args = {"check_same_thread": False} if db_uri.startswith("sqlite") else {}

    _engine = create_engine(db_uri, connect_args=connect_args, future=True)
    SessionLocal.configure(bind=_engine)
    Base.metadata.create_all(bind=_engine)


def get_session() -> Session:
    return SessionLocal()


def close_session(exception: BaseException | None = None) -> None:
    SessionLocal.remove()