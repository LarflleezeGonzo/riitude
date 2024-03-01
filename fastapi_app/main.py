from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute

from .api.api import api_router
from .api.dependencies import Base, engine
from .core.config import settings
from .core.response_handlers import (
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix=settings.API_V1_STR)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
