"""Service layer for model loading and risk prediction."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from backend.core.exceptions import ArtifactNotFoundError, PredictionError
from backend.services.nlp_service import NLPService

logger = logging.getLogger(__name__)


class ModelService:
    def __init__(self, model_path: str, preprocessor_path: str, label_encoder_path: str):
        self.model_path = model_path
        self.preprocessor_path = preprocessor_path
        self.label_encoder_path = label_encoder_path

        self._validate_artifacts()
        self.model = joblib.load(model_path)
        self.preprocessor = joblib.load(preprocessor_path)
        self.label_encoder = joblib.load(label_encoder_path)
        self.nlp = NLPService()

    def _validate_artifacts(self) -> None:
        for artifact in [self.model_path, self.preprocessor_path, self.label_encoder_path]:
            if not Path(artifact).exists():
                raise ArtifactNotFoundError(f"Missing model artifact: {artifact}. Run training first.")

    def is_model_loaded(self) -> bool:
        return all(hasattr(self, attr) for attr in ["model", "preprocessor", "label_encoder"])

    def predict(self, payload: dict[str, Any], headlines: list[str]) -> dict[str, Any]:
        try:
            df = pd.DataFrame([payload])
            probs = self.model.predict_proba(df)[0]
            pred_idx = int(probs.argmax())
            risk_label = str(self.label_encoder.inverse_transform([pred_idx])[0])
        except Exception as exc:  # noqa: BLE001
            logger.exception("Prediction pipeline failed")
            raise PredictionError("Unable to generate risk prediction from supplied features") from exc

        base_score_map = {"Low": 0.2, "Medium": 0.5, "High": 0.85}
        nlp_result = self.nlp.analyze(headlines)
        risk_score = min(max(base_score_map[risk_label] + nlp_result.risk_adjustment, 0.0), 1.0)

        feature_values = df.iloc[0].to_dict()
        importance = [{"feature": k, "value": float(abs(v))} for k, v in feature_values.items() if isinstance(v, (int, float))]
        importance = sorted(importance, key=lambda i: i["value"], reverse=True)[:5]

        return {
            "risk_level": risk_label,
            "confidence": float(probs[pred_idx]),
            "risk_score": risk_score,
            "nlp_signal": {
                "sentiment": nlp_result.sentiment,
                "risk_adjustment": nlp_result.risk_adjustment,
                "summary": nlp_result.summary,
            },
            "explanation": {
                "positive_contributors": importance[:3],
                "negative_contributors": [],
                "importance_values": importance,
            },
        }
