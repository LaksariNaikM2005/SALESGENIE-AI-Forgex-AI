import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SQLITE_PATH = PROJECT_ROOT / "database" / "forge_x_ai.db"


class Settings(BaseSettings):
    app_name: str = "FORGE_X_AI"
    app_env: str = "development"
    debug: bool = True

    # Database: Default to PostgreSQL, with auto-fallback to SQLite for seamless local dev
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/salesgenie",
    )
    fallback_database_url: str = f"sqlite:///{SQLITE_PATH.as_posix()}"

    # Redis & Celery
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    celery_broker_url: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    celery_result_backend: str = os.getenv(
        "CELERY_RESULT_BACKEND", "redis://localhost:6379/1"
    )

    # Security
    jwt_secret_key: str = os.getenv(
        "JWT_SECRET_KEY", "q4Tvn-StGSzlLr8JB83RwohGeC-r3mDLYlumZEq3Pw9R0ZJuhmuJiWjfjQrxNPGOnG5J3hlz4mK3imvElxnm5A"
    )
    access_token_expire_minutes: int = 1440  # 24 hours

    # External APIs
    gemini_api_key: Optional[str] = os.getenv("Gemini_API_Key", "")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()


def create_db_engine():
    """
    Creates an engine targeting PostgreSQL by default. If PostgreSQL is unreachable
    during local developer mode (without Docker started), gracefully falls back to SQLite
    so local execution and test suites never break.
    """
    target_url = settings.database_url
    try:
        if target_url.startswith("postgresql"):
            # Test engine connectivity
            test_engine = create_engine(target_url, pool_pre_ping=True, connect_args={"connect_timeout": 2})
            with test_engine.connect() as conn:
                pass
            return test_engine
    except Exception as exc:
        print(f"[Database] PostgreSQL connection failed ({exc}). Falling back to SQLite: {settings.fallback_database_url}")
        target_url = settings.fallback_database_url

    if target_url.startswith("sqlite"):
        # SQLite parameters
        return create_engine(
            target_url,
            connect_args={"check_same_thread": False},
        )

    return create_engine(target_url, pool_pre_ping=True)


engine = create_db_engine()

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)

ScopedSession = scoped_session(SessionLocal)


class QueryProperty:
    def __get__(self, instance, owner):
        if owner is None:
            return self
        return ScopedSession.query(owner)


class Base(DeclarativeBase):
    pass


Base.query = QueryProperty()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)