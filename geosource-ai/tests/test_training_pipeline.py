import joblib

from backend.core.config import settings
from backend.models.train import main


def test_training_persists_artifacts() -> None:
    main()
    model = joblib.load(settings.model_path)
    encoder = joblib.load(settings.label_encoder_path)
    assert hasattr(model, "predict_proba")
    assert set(encoder.classes_.tolist()) == {"Low", "Medium", "High"}
