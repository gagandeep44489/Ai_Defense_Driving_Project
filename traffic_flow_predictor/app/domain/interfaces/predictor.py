from abc import ABC, abstractmethod
from typing import Any


class Predictor(ABC):
    @abstractmethod
    async def predict(self, X: Any):
        ...

    @abstractmethod
    async def train(self, X: Any, y: Any):
        ...
