from fastapi import APIRouter, Depends, HTTPException
from redis.asyncio import Redis

from app.core.cache import get_redis_client
from app.core.config import settings
from app.infrastructure.models.random_forest_model import RandomForestModel
from app.infrastructure.repository.model_repository import ModelRepository
from app.schemas.request import TrafficRequest
from app.schemas.response import TrafficResponse
from app.services.prediction_service import PredictionService
from app.services.preprocessing_service import PreprocessingService

router = APIRouter()


async def get_prediction_service(cache: Redis = Depends(get_redis_client)) -> PredictionService:
    repository = ModelRepository(settings.MODEL_PATH)
    try:
        artifact = await repository.load()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail="Model not trained. Run training pipeline first.") from exc

    predictor = RandomForestModel(artifact["model"])
    preprocessor = PreprocessingService()
    return PredictionService(predictor, preprocessor, artifact["feature_columns"], artifact["stats"], cache)


@router.post("/predict", response_model=TrafficResponse)
async def predict_traffic(request: TrafficRequest, service: PredictionService = Depends(get_prediction_service)) -> TrafficResponse:
    return await service.predict(request)
