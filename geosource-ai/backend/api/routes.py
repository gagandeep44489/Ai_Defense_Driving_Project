"""FastAPI routes for GeoSource AI backend."""
from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from backend.core.config import settings
from backend.schemas.supplier import (
    HealthResponse,
    PredictRequest,
    PredictResponse,
    RecommendRequest,
    RecommendResponse,
)
from backend.services.graph_service import GraphService
from backend.services.model_service import ModelService

logger = logging.getLogger(__name__)
router = APIRouter(tags=["GeoSource AI"])


def get_model_service() -> ModelService:
    return ModelService(settings.model_path, settings.preprocessor_path, settings.label_encoder_path)


def get_graph_service() -> GraphService:
    return GraphService(settings.graph_path, settings.data_path)


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    try:
        svc = get_model_service()
        loaded = svc.is_model_loaded()
    except Exception:  # noqa: BLE001
        loaded = False
    return HealthResponse(status="ok", service=settings.app_name, model_loaded=loaded)


@router.post("/predict-risk", response_model=PredictResponse)
async def predict_risk(req: PredictRequest, svc: ModelService = Depends(get_model_service)) -> PredictResponse:
    logger.info("Prediction request received for country=%s", req.supplier.country)
    result = svc.predict(req.supplier.model_dump(exclude={"supplier_id"}), req.headlines)
    return PredictResponse(**result)


@router.post("/recommend", response_model=RecommendResponse)
async def recommend(req: RecommendRequest, svc: GraphService = Depends(get_graph_service)) -> RecommendResponse:
    logger.info("Recommendation request received for supplier=%s", req.supplier_id)
    return RecommendResponse(alternatives=svc.recommend(req.supplier_id, req.top_k))


@router.get("/graph-summary")
async def graph_summary(svc: GraphService = Depends(get_graph_service)) -> dict:
    return svc.summary()
