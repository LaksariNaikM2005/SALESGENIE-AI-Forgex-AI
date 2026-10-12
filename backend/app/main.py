from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import settings, init_db
from .api.auth import router as auth_router
from .api.admin_users import router as admin_users_router
from .api.leads import router as leads_router
from .api.analytics import router as analytics_router
from .api.recommendations import router as recommendations_router
from .api.outreach import router as outreach_router
from .api.followups import router as followups_router
from .api.conversations import router as conversations_router
from .api.crm import router as crm_router
from .api.tasks import router as tasks_router
from .services.lead_service import auto_seed_leads_if_empty
from .core.redis_client import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables created and initial dataset ready
    try:
        init_db()
        auto_seed_leads_if_empty()
    except Exception as exc:
        print(f"[Startup Warning] Could not auto-seed database: {exc}")
    yield
    # Shutdown


app = FastAPI(
    title="SalesGenie AI — Modern Enterprise API",
    description="High-performance FastAPI Backend for B2B Industrial Manufacturing Sales Intelligence & Qualification",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_router)
app.include_router(admin_users_router)
app.include_router(leads_router)
app.include_router(analytics_router)
app.include_router(recommendations_router)
app.include_router(outreach_router)
app.include_router(followups_router)
app.include_router(conversations_router)
app.include_router(crm_router)
app.include_router(tasks_router)


@app.get("/")
def index():
    return {
        "service": settings.app_name,
        "framework": "FastAPI",
        "database": "PostgreSQL",
        "cache": "Redis",
        "background_jobs": "Celery",
        "status": "healthy",
        "docs": "/docs",
        "health": "/api/health",
    }


@app.get("/health")
@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": settings.app_name,
        "database": "connected",
        "redis_available": redis_client.is_available,
    }