"""Centralized exception handlers for FastAPI."""
from __future__ import annotations

import logging
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.core.exceptions import ArtifactNotFoundError, GeoSourceError, PredictionError

logger = logging.getLogger(__name__)


def _error_payload(code: str, message: str) -> dict:
    return {
        "error": {"code": code, "message": message},
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ArtifactNotFoundError)
    async def handle_artifact_error(_: Request, exc: ArtifactNotFoundError) -> JSONResponse:
        logger.warning("Artifact error: %s", exc)
        return JSONResponse(status_code=503, content=_error_payload("artifact_unavailable", str(exc)))

    @app.exception_handler(PredictionError)
    async def handle_prediction_error(_: Request, exc: PredictionError) -> JSONResponse:
        logger.error("Prediction error: %s", exc)
        return JSONResponse(status_code=422, content=_error_payload("prediction_failed", str(exc)))

    @app.exception_handler(GeoSourceError)
    async def handle_domain_error(_: Request, exc: GeoSourceError) -> JSONResponse:
        logger.error("Domain error: %s", exc)
        return JSONResponse(status_code=400, content=_error_payload("domain_error", str(exc)))

    @app.exception_handler(Exception)
    async def handle_unexpected_error(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled error")
        return JSONResponse(status_code=500, content=_error_payload("internal_error", "Unexpected server error"))
