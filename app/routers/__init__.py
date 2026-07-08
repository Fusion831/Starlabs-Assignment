from app.routers.auth import router as auth_router
from app.routers.classes import router as classes_router
from app.routers.bookings import router as bookings_router

__all__ = ["auth_router", "classes_router", "bookings_router"]
