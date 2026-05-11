from fastapi import APIRouter
from app.presentation.api.v1.routers import analytics, auth, skillgap
api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(skillgap.router)
api_router.include_router(analytics.router)
