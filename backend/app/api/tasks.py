from typing import Annotated
from fastapi import APIRouter, Depends
from celery.result import AsyncResult

from .auth import get_current_user
from ..celery_app import celery_app
from ..models import User

router = APIRouter(prefix="/api/tasks", tags=["Background Tasks"])
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("/{task_id}")
def get_task_status(
    task_id: str,
    current_user: CurrentUser,
):
    """
    Checks the status and result of a Celery background job by task_id.
    """
    result = AsyncResult(task_id, app=celery_app)
    response = {
        "task_id": task_id,
        "status": result.status,
        "ready": result.ready(),
        "successful": result.successful() if result.ready() else None,
    }
    if result.ready():
        if result.successful():
            response["result"] = result.result
        else:
            response["error"] = str(result.result)

    return response
