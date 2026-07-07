"""FastAPI application factory for SovereignAI."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from starlette.responses import Response
from sovereignai.api.v1.routes import router as v1_router
from sovereignai.config.settings import get_settings

SECURITY_HEADERS = {'X-Content-Type-Options':'nosniff','X-Frame-Options':'DENY','Referrer-Policy':'no-referrer','Content-Security-Policy':"default-src 'self'"}

def create_app() -> FastAPI:
    """Create and configure the API app."""
    settings=get_settings(); app=FastAPI(title=settings.app_name, version='0.1.0', docs_url='/docs', openapi_url='/openapi.json')
    app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=['GET','POST','PUT','DELETE'], allow_headers=['Authorization','Content-Type'])
    @app.middleware('http')
    async def add_security_headers(request, call_next):  # type: ignore[no-untyped-def]
        response = await call_next(request)
        for k,v in SECURITY_HEADERS.items(): response.headers[k]=v
        return response
    @app.get('/health', tags=['operations'])
    def health() -> dict[str,str]:
        """Return service health."""
        return {'status':'ok','service':settings.app_name}
    @app.get('/metrics', tags=['operations'])
    def metrics() -> Response:
        """Expose Prometheus metrics."""
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
    app.include_router(v1_router, prefix='/api/v1')
    return app

app = create_app()
