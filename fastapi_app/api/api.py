from fastapi import APIRouter

from .endpoints.books import router as books_router
from .endpoints.ping import router as ping_router

api_router = APIRouter()
api_router.include_router(books_router, tags=["Books & Reviews"])
api_router.include_router(ping_router, tags=["General APIs"])
