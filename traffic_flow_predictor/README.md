# Traffic Flow Predictor (FastAPI + Async + Redis)

## Clean Architecture
```text
API Layer: app/api/v1/endpoints/prediction.py
Service Layer: app/services/prediction_service.py, preprocessing_service.py
Domain Layer: app/domain/interfaces/predictor.py
Infrastructure Layer: app/infrastructure/models, app/infrastructure/repository, app/core/cache.py
```

## Redis Caching
- Redis async client from `redis.asyncio` in `app/core/cache.py`.
- Cache key strategy: deterministic SHA256 hash of request JSON.
- Key format: `traffic:{hash}`.
- TTL: 300 seconds (`CACHE_TTL_SECONDS`).
- Cache flow in `PredictionService`:
  1) generate key
  2) `await redis.get(key)`
  3) if miss -> preprocess + model predict
  4) store with `await redis.set(..., ex=300)`
  5) return response with `cached` flag
- Redis failure fallback: gracefully bypass cache and return model prediction.

## Async Design
- All endpoints and service operations are async.
- Sklearn sync methods wrapped with `loop.run_in_executor()`.
- Redis operations are awaited and non-blocking.

## Run Instructions
```bash
docker run -d -p 6379:6379 redis
pip install -r requirements.txt
python pipelines/training_pipeline.py
uvicorn app.main:app --reload
```
