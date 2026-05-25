"""Prediction utilities for offline/CLI usage."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from backend.core.config import settings


@dataclass
class PredictionResult:
    risk_level: str
    confidence: float


class PredictionEngine:
    """Utility wrapper around persisted training artifacts."""

    def __init__(self, model_path: str, label_encoder_path: str):
        self.model_path = model_path
        self.label_encoder_path = label_encoder_path
        self._validate_artifacts()
        self.model = joblib.load(model_path)
        self.label_encoder = joblib.load(label_encoder_path)

    def _validate_artifacts(self) -> None:
        for artifact in [self.model_path, self.label_encoder_path]:
            if not Path(artifact).exists():
                raise FileNotFoundError(f"Missing artifact: {artifact}")

    def predict_one(self, features: dict[str, Any]) -> PredictionResult:
        frame = pd.DataFrame([features])
        probabilities = self.model.predict_proba(frame)[0]
        predicted_index = int(probabilities.argmax())
        risk_level = str(self.label_encoder.inverse_transform([predicted_index])[0])
        return PredictionResult(risk_level=risk_level, confidence=float(probabilities[predicted_index]))


def load_default_engine() -> PredictionEngine:
    return PredictionEngine(settings.model_path, settings.label_encoder_path)
