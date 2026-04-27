"""Train and use supplier risk prediction model."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple
import pickle

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "data" / "suppliers.csv"
MODEL_PATH = ROOT_DIR / "models" / "risk_model.pkl"

FEATURES = [
    "country",
    "cost",
    "delivery_time",
    "reliability_score",
    "defect_rate",
    "delay_history",
]
TARGET = "risk_label"


def train_and_save_model(data_path: Path = DATA_PATH, model_path: Path = MODEL_PATH) -> Dict[str, str]:
    """Train risk classifier and persist artifact."""
    df = pd.read_csv(data_path)
    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["country"]),
            (
                "num",
                "passthrough",
                ["cost", "delivery_time", "reliability_score", "defect_rate", "delay_history"],
            ),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=300,
                    max_depth=12,
                    random_state=42,
                    class_weight="balanced",
                ),
            ),
        ]
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    report = classification_report(y_test, predictions, output_dict=True)

    model_path.parent.mkdir(parents=True, exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    return {
        "accuracy": f"{report['accuracy']:.3f}",
        "macro_f1": f"{report['macro avg']['f1-score']:.3f}",
        "model_path": str(model_path),
    }


def load_model(model_path: Path = MODEL_PATH) -> Pipeline:
    """Load serialized classifier artifact."""
    if not model_path.exists():
        train_and_save_model(model_path=model_path)

    with open(model_path, "rb") as f:
        return pickle.load(f)


def predict_risk(input_data: Dict) -> str:
    """Predict risk label from a single supplier feature payload."""
    model = load_model()
    df = pd.DataFrame([input_data])
    pred = model.predict(df)[0]
    return str(pred)


if __name__ == "__main__":
    metrics = train_and_save_model()
    print("Training complete:", metrics)
