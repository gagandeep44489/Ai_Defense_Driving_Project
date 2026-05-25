import joblib
import pandas as pd

from backend.services.nlp_service import NLPService


class ModelService:
    labels = ["Low", "Medium", "High"]

    def __init__(self, model_path: str, preprocessor_path: str):
        self.model = joblib.load(model_path)
        self.preprocessor = joblib.load(preprocessor_path)
        self.nlp = NLPService()

    def predict(self, payload: dict, headlines: list[str]) -> dict:
        df = pd.DataFrame([payload])
        x = self.preprocessor.transform(df)
        probs = self.model.predict_proba(x)[0]
        idx = int(probs.argmax())
        base_score = float(idx / 2)
        nlp_result = self.nlp.analyze(headlines)
        risk_score = min(max(base_score + nlp_result.risk_adjustment, 0.0), 1.0)
        top = sorted(zip(df.columns.tolist(), x.toarray()[0] if hasattr(x, 'toarray') else x[0]), key=lambda t: abs(float(t[1])), reverse=True)[:5]
        return {
            "risk_level": self.labels[idx],
            "confidence": float(probs[idx]),
            "risk_score": risk_score,
            "explanation": {
                "positive_contributors": [{"feature": f, "value": float(v)} for f, v in top if float(v) > 0][:3],
                "negative_contributors": [{"feature": f, "value": float(v)} for f, v in top if float(v) < 0][:3],
                "importance_values": [{"feature": f, "value": abs(float(v))} for f, v in top],
            },
        }
