import hashlib
import json
from redis.exceptions import RedisError
from redis.asyncio import Redis

from app.core.config import settings
from app.domain.interfaces.predictor import Predictor
from app.schemas.request import TrafficRequest
from app.schemas.response import TrafficResponse
from app.services.preprocessing_service import PreprocessingService


class PredictionService:
    def __init__(self, predictor: Predictor, preprocessing_service: PreprocessingService, feature_columns: list[str], stats: dict, cache: Redis):
        self.predictor = predictor
        self.preprocessing_service = preprocessing_service
        self.feature_columns = feature_columns
        self.stats = stats
        self.cache = cache

    def _cache_key(self, request: TrafficRequest) -> str:
        raw = request.model_dump_json()
        digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        return f"traffic:{digest}"

    async def predict(self, request: TrafficRequest) -> TrafficResponse:
        key = self._cache_key(request)

        try:
            cached = await self.cache.get(key)
            if cached:
                payload = json.loads(cached)
                return TrafficResponse(**payload, cached=True)
        except RedisError:
            pass

        model_input = await self.preprocessing_service.transform_request(request, self.feature_columns, self.stats)
        predicted = float((await self.predictor.predict(model_input))[0])
        category = "Low" if predicted < 2000 else "Medium" if predicted <= 5000 else "High"
        response = TrafficResponse(prediction=round(predicted, 2), category=category, cached=False)

        try:
            await self.cache.set(key, json.dumps(response.model_dump(exclude={"cached"})), ex=settings.CACHE_TTL_SECONDS)
        except RedisError:
            pass

        return response
