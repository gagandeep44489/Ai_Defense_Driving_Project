from fastapi import APIRouter
from app.api.v1 import actions, analytics, auth, meetings, notifications, search

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(meetings.router)
api_router.include_router(actions.router)
api_router.include_router(search.router)
api_router.include_router(analytics.router)
api_router.include_router(notifications.router)
