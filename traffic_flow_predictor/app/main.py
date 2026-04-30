from fastapi import FastAPI

from app.api.v1.endpoints.prediction import router as prediction_router

app = FastAPI(title="Traffic Flow Predictor", version="2.0.0")
app.include_router(prediction_router)
