"""FastAPI application entrypoint."""
from __future__ import annotations

from fastapi import FastAPI

from backend.api.routes import router
from backend.core.config import settings
from backend.core.logging import configure_logging
from backend.middleware.exception_handlers import register_exception_handlers

configure_logging(settings.log_level)
app = FastAPI(title=settings.app_name, version=settings.model_version)
register_exception_handlers(app)
app.include_router(router, prefix=settings.api_prefix)
