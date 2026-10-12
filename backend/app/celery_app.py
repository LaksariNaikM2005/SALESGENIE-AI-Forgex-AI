import os
import logging
from celery import Celery

from .database import settings

logger = logging.getLogger("celery_tasks")

# Initialize Celery app instance
celery_app = Celery(
    "salesgenie_tasks",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["backend.app.tasks.lead_tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    broker_connection_retry_on_startup=True,
    # If Redis is unavailable during local unit tests or offline dev, execute eagerly
    task_always_eager=os.getenv("CELERY_ALWAYS_EAGER", "false").lower() == "true",
)

if __name__ == "__main__":
    celery_app.start()
