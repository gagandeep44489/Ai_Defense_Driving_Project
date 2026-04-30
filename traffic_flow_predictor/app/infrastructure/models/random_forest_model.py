import asyncio
from concurrent.futures import Executor
from typing import Any

from sklearn.ensemble import RandomForestRegressor

from app.domain.interfaces.predictor import Predictor


class RandomForestModel(Predictor):
    def __init__(self, model: RandomForestRegressor | None = None, executor: Executor | None = None):
        self._model = model or RandomForestRegressor(n_estimators=250, random_state=42, n_jobs=-1)
        self._executor = executor

    async def train(self, X: Any, y: Any):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(self._executor, self._model.fit, X, y)

    async def predict(self, X: Any):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self._executor, self._model.predict, X)

    @property
    def native_model(self) -> RandomForestRegressor:
        return self._model
