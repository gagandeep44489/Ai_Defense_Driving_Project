from pathlib import Path
import os


class Settings:
    BASE_DIR = Path(__file__).resolve().parents[2]
    MODEL_PATH = BASE_DIR / "model.pkl"
    DATA_PATH = BASE_DIR / "traffic_dataset.csv"
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CACHE_TTL_SECONDS = 300


settings = Settings()
