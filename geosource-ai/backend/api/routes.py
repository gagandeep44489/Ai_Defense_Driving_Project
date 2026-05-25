"""API routes for GeoSource AI."""
from fastapi import APIRouter, Depends, HTTPException

from backend.core.config import settings
from backend.schemas.supplier import PredictRequest, PredictResponse, RecommendRequest, RecommendResponse
from backend.services.graph_service import GraphService
from backend.services.model_service import ModelService

router = APIRouter()


def get_model_service() -> ModelService:
    try:
        return ModelService(settings.model_path, settings.preprocessor_path, settings.label_encoder_path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


def get_graph_service() -> GraphService:
    return GraphService(settings.graph_path, settings.data_path)


@router.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@router.get("/model-info")
async def model_info() -> dict:
    return {"model_version": settings.model_version, "model_type": "XGBoostClassifier"}


@router.post("/predict-risk", response_model=PredictResponse)
async def predict_risk(req: PredictRequest, svc: ModelService = Depends(get_model_service)) -> PredictResponse:
    result = svc.predict(req.supplier.model_dump(exclude={"supplier_id"}), req.headlines)
    return PredictResponse(**result)


@router.post("/recommend", response_model=RecommendResponse)
async def recommend(req: RecommendRequest, svc: GraphService = Depends(get_graph_service)) -> RecommendResponse:
    return RecommendResponse(alternatives=svc.recommend(req.supplier_id, req.top_k))


@router.get("/graph-summary")
async def graph_summary(svc: GraphService = Depends(get_graph_service)) -> dict:
    return svc.summary()
