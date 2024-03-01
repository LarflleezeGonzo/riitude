import sys
from typing import Any, Optional

from fastapi import HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class CustomResponse(BaseModel):
    """
    Custom response model for consistent response format.
    """

    status: str
    data: Any
    message: str
    statusCode: Optional[int]


class NotFoundException(HTTPException):
    """
    Custom exception class for representing resource not found.
    """

    def __init__(self, detail: str = "Requested resource not found"):
        """
        Initializes the NotFoundException.

        Args:
            detail (str): Detail message for the exception.
        """
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


def custom_response(
    status: str, message: str, code: Optional[int] = None, data: Any = None
) -> JSONResponse:
    """
    Generates a custom JSON response.

    Args:
        status (str): Status of the response.
        message (str): Response message.
        code (Optional[int]): HTTP status code.
        data (Any): Additional data in the response.

    Returns:
        JSONResponse: FastAPI JSONResponse object.
    """
    response = CustomResponse(
        status=status, message=message, statusCode=code, data=jsonable_encoder(data)
    )
    return JSONResponse(status_code=code, content=dict(response))


def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Handles validation exceptions.

    Args:
        request (Request): The FastAPI request object.
        exc (RequestValidationError): The validation exception.

    Returns:
        JSONResponse: FastAPI JSONResponse object.
    """
    details = exc.errors()
    modified_details = []

    for error in details:
        modified_details.append(
            {
                "loc": error["loc"],
                "message": error["msg"],
                "type": error["type"],
            }
        )

    url = (
        f"{request.url.path}?{request.query_params}"
        if request.query_params
        else request.url.path
    )

    return custom_response(
        "fail",
        "Validation error",
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        data={"detail": modified_details, "url": url, "method": request.method},
    )


def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handles HTTP exceptions.

    Args:
        request (Request): The FastAPI request object.
        exc (HTTPException): The HTTP exception.

    Returns:
        JSONResponse: FastAPI JSONResponse object.
    """
    url = (
        f"{request.url.path}?{request.query_params}"
        if request.query_params
        else request.url.path
    )

    return custom_response(
        "fail",
        exc.detail,
        exc.status_code,
        data={"url": url, "method": request.method},
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handles unhandled exceptions.

    Args:
        request (Request): The FastAPI request object.
        exc (Exception): The unhandled exception.

    Returns:
        JSONResponse: FastAPI JSONResponse object.
    """
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    url = (
        f"{request.url.path}?{request.query_params}"
        if request.query_params
        else request.url.path
    )
    exception_type, exception_value, _ = sys.exc_info()
    exception_name = getattr(exception_type, "__name__", None)
    detail = f'{host}:{port} - "{request.method} {url}" 500 Internal Server Error <{exception_name}: {exception_value} {str(exc)}>'

    return custom_response("error", detail, 500)


def success_response(
    message: str = "Operation successful",
    code: Optional[int] = status.HTTP_200_OK,
    data: Any = None,
):
    return custom_response("success", message, code, data)
