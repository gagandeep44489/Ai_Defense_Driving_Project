from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from starlette.responses import JSONResponse
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.presentation.api.v1.api import api_router
configure_logging(); settings = get_settings(); limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title=settings.app_name, version="0.1.0", docs_url="/api/docs", openapi_url="/api/openapi.json")
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origin_list, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(_: Request, exc: RateLimitExceeded): return JSONResponse(status_code=429, content={"detail": str(exc)})
@app.get("/health", tags=["system"])
async def health() -> dict: return {"status": "ok", "environment": settings.environment}
app.include_router(api_router)
