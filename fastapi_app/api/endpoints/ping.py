from typing import Any

from fastapi import APIRouter
from ...core.response_handlers import success_response

router = APIRouter()


@router.get("/ping")
def ping() -> Any:
    """
    Ping API.
    """

    return success_response(message="Application is Up!")