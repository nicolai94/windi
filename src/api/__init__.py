from fastapi import APIRouter

from src.core.config import settings
from src.api.routers.auth import router as auth_router
from src.api.routers.chat import router as chat_router

router = APIRouter(
    prefix=settings.api.prefix,
)
router.include_router(auth_router, prefix=settings.api.auth)
router.include_router(chat_router, prefix=settings.api.chat)
