"""Explainability helpers for per-prediction feature contributions."""
from __future__ import annotations

from typing import Dict, List

import pandas as pd

from backend.risk_model import load_model


FEATURE_ORDER = [
    "country",
    "cost",
    "delivery_time",
    "reliability_score",
    "defect_rate",
    "delay_history",
]


def _fallback_explanation(input_data: Dict) -> List[Dict]:
    """Lightweight deterministic explanation when SHAP is unavailable."""
    reliability_penalty = (100.0 - float(input_data["reliability_score"])) / 100.0
    contributions = {
        "cost": float(input_data["cost"]) / 220.0,
        "delivery_time": float(input_data["delivery_time"]) / 35.0,
        "defect_rate": float(input_data["defect_rate"]) / 12.0,
        "delay_history": float(input_data["delay_history"]) / 20.0,
        "reliability_score": reliability_penalty,
        "country": 0.1,
    }
    return [
        {"feature": k, "impact": round(v, 4)}
        for k, v in sorted(contributions.items(), key=lambda item: abs(item[1]), reverse=True)
    ]


def explain_prediction(input_data: Dict) -> List[Dict]:
    """Return sorted feature impacts using SHAP values when available."""
    model = load_model()
    row_df = pd.DataFrame([input_data])[FEATURE_ORDER]

    try:
        import shap  # type: ignore

        classifier = model.named_steps["classifier"]
        transformed = model.named_steps["preprocessor"].transform(row_df)
        explainer = shap.TreeExplainer(classifier)
        shap_values = explainer.shap_values(transformed)

        if isinstance(shap_values, list):
            # Multiclass: pick class with highest predicted probability
            probs = classifier.predict_proba(transformed)[0]
            class_idx = int(probs.argmax())
            row_shap = shap_values[class_idx][0]
        else:
            row_shap = shap_values[0]

        feature_names = model.named_steps["preprocessor"].get_feature_names_out()
        items = [
            {"feature": str(name), "impact": float(value)}
            for name, value in zip(feature_names, row_shap)
        ]
        items.sort(key=lambda x: abs(x["impact"]), reverse=True)
        return items[:10]
    except Exception:
        return _fallback_explanation(input_data)
