"""Model inference service."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from backend.services.nlp_service import NLPService


class ModelService:
    def __init__(self, model_path: str, preprocessor_path: str, label_encoder_path: str):
        for artifact in [model_path, preprocessor_path, label_encoder_path]:
            if not Path(artifact).exists():
                raise FileNotFoundError(f"Missing model artifact: {artifact}. Run training first.")

        self.model = joblib.load(model_path)
        self.preprocessor = joblib.load(preprocessor_path)
        self.label_encoder = joblib.load(label_encoder_path)
        self.nlp = NLPService()

    def predict(self, payload: dict[str, Any], headlines: list[str]) -> dict[str, Any]:
        df = pd.DataFrame([payload])
        x = self.preprocessor.transform(df)
        probs = self.model.predict_proba(x)[0]
        pred_idx = int(probs.argmax())
        risk_label = str(self.label_encoder.inverse_transform([pred_idx])[0])

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
