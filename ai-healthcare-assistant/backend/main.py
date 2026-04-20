from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.healthcare import router as healthcare_router
from utils.logger import setup_logging

setup_logging()

app = FastAPI(title="AI Healthcare Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(healthcare_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
