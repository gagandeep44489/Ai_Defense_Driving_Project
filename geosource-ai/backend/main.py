from fastapi import FastAPI

from backend.api.routes import router
from backend.core.config import settings
from backend.core.logging import configure_logging

configure_logging(settings.log_level)
app = FastAPI(title=settings.app_name)
app.include_router(router, prefix=settings.api_prefix)
