"""Training pipeline for GeoSource AI supplier risk classification."""
from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path

import joblib
import networkx as nx
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from xgboost import XGBClassifier

from backend.core.config import settings

logger = logging.getLogger(__name__)

TARGET_COLUMN = "risk_level"
FEATURE_COLUMNS = ["country", "cost", "delivery_time", "reliability_score", "defect_rate", "delay_history"]
EXPECTED_CLASSES = {"Low", "Medium", "High"}


@dataclass
class TrainingMetrics:
    """Serializable training outputs for monitoring and reproducibility."""

    accuracy: float
    f1_macro: float
    classification_report: dict
    confusion_matrix: list[list[int]]


def build_preprocessor() -> ColumnTransformer:
    """Build reusable preprocessing graph with encoding and scaling."""
    return ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["country"]),
            (
                "num",
                StandardScaler(),
                [feature for feature in FEATURE_COLUMNS if feature != "country"],
            ),
        ]
    )


def build_model(num_class: int) -> XGBClassifier:
    """Build multiclass XGBoost classifier."""
    return XGBClassifier(
        objective="multi:softprob",
        num_class=num_class,
        eval_metric="mlogloss",
        n_estimators=220,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.9,
        colsample_bytree=0.9,
        random_state=42,
    )


def build_graph(df: pd.DataFrame) -> nx.Graph:
    """Build supplier similarity graph for recommendation service."""
    graph = nx.Graph()
    for _, row in df.iterrows():
        graph.add_node(row.supplier_id, country=row.country, risk=row.risk_level)

    rows = df.to_dict("records")
    for i, left in enumerate(rows):
        for right in rows[i + 1 :]:
            similar = (
                left["country"] == right["country"]
                or abs(left["cost"] - right["cost"]) < 100
                or abs(left["reliability_score"] - right["reliability_score"]) < 10
            )
            if similar:
                graph.add_edge(left["supplier_id"], right["supplier_id"])
    return graph


def validate_training_frame(df: pd.DataFrame) -> None:
    """Validate incoming training frame columns and class coverage."""
    missing_columns = [column for column in FEATURE_COLUMNS + [TARGET_COLUMN] if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Training data missing required columns: {missing_columns}")

    actual_classes = set(df[TARGET_COLUMN].dropna().unique().tolist())
    if actual_classes != EXPECTED_CLASSES:
        raise ValueError(f"Expected classes {sorted(EXPECTED_CLASSES)} but found {sorted(actual_classes)}")


def train_pipeline(df: pd.DataFrame) -> tuple[Pipeline, LabelEncoder, TrainingMetrics]:
    """Train pipeline and return fitted estimator, encoder, and metrics."""
    validate_training_frame(df)

    x = df[FEATURE_COLUMNS]
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df[TARGET_COLUMN])

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model_pipeline = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            ("classifier", build_model(num_class=len(label_encoder.classes_))),
        ]
    )
    model_pipeline.fit(x_train, y_train)

    predictions = model_pipeline.predict(x_test)
    report = classification_report(
        y_test,
        predictions,
        target_names=label_encoder.classes_,
        output_dict=True,
        zero_division=0,
    )

    metrics = TrainingMetrics(
        accuracy=float(accuracy_score(y_test, predictions)),
        f1_macro=float(f1_score(y_test, predictions, average="macro")),
        classification_report=report,
        confusion_matrix=confusion_matrix(y_test, predictions).tolist(),
    )
    return model_pipeline, label_encoder, metrics


def persist_artifacts(
    model_pipeline: Pipeline,
    label_encoder: LabelEncoder,
    metrics: TrainingMetrics,
    training_frame: pd.DataFrame,
) -> None:
    """Save model artifacts, metrics, and graph to disk."""
    model_dir = Path("models")
    model_dir.mkdir(parents=True, exist_ok=True)

    joblib.dump(model_pipeline, settings.model_path)
    joblib.dump(model_pipeline.named_steps["preprocessor"], settings.preprocessor_path)
    joblib.dump(label_encoder, settings.label_encoder_path)
    joblib.dump(build_graph(training_frame), settings.graph_path)

    metrics_path = model_dir / "training_metrics.json"
    metrics_path.write_text(json.dumps(asdict(metrics), indent=2), encoding="utf-8")

    logger.info("Saved model pipeline: %s", settings.model_path)
    logger.info("Saved label encoder: %s", settings.label_encoder_path)
    logger.info("Saved training metrics: %s", metrics_path)


def main() -> None:
    """Train and persist artifacts for risk prediction inference."""
    logging.basicConfig(level=settings.log_level, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    logger.info("Loading training data from %s", settings.data_path)
    training_frame = pd.read_csv(settings.data_path)

    model_pipeline, label_encoder, metrics = train_pipeline(training_frame)
    persist_artifacts(model_pipeline, label_encoder, metrics, training_frame)

    logger.info("Training completed with accuracy=%.4f f1_macro=%.4f", metrics.accuracy, metrics.f1_macro)


if __name__ == "__main__":
    main()
