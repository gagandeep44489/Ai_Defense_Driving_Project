import asyncio
from pathlib import Path

import joblib


class ModelRepository:
    def __init__(self, model_path: Path):
        self._model_path = model_path
        self._artifact_cache: dict | None = None

    async def save(self, artifact: dict) -> None:
        self._model_path.parent.mkdir(parents=True, exist_ok=True)
        await asyncio.to_thread(joblib.dump, artifact, self._model_path)
        self._artifact_cache = artifact

    async def load(self) -> dict:
        if self._artifact_cache is not None:
            return self._artifact_cache
        if not self._model_path.exists():
            raise FileNotFoundError(f"Model file not found: {self._model_path}")
        artifact = await asyncio.to_thread(joblib.load, self._model_path)
        self._artifact_cache = artifact
        return artifact
