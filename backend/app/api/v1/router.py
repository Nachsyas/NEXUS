from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.health import router as health_router
from app.api.v1.users import router as users_router

api_router = APIRouter()
api_router.include_router(health_router, prefix="", tags=["Health"])
api_router.include_router(auth_router, prefix="", tags=["Auth & Identity"])
api_router.include_router(users_router, prefix="", tags=["User & Preferences"])
