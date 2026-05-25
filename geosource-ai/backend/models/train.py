"""Training pipeline for supplier risk model."""
from __future__ import annotations

import logging
from pathlib import Path

import joblib
import networkx as nx
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from xgboost import XGBClassifier

from backend.core.config import settings

logger = logging.getLogger(__name__)


FEATURE_COLUMNS = ["country", "cost", "delivery_time", "reliability_score", "defect_rate", "delay_history"]


def build_graph(df: pd.DataFrame) -> nx.Graph:
    g = nx.Graph()
    for _, row in df.iterrows():
        g.add_node(row.supplier_id, country=row.country, risk=row.risk_level)
    rows = df.to_dict("records")
    for i, a in enumerate(rows):
        for b in rows[i + 1 :]:
            similar = (
                a["country"] == b["country"]
                or abs(a["cost"] - b["cost"]) < 100
                or abs(a["reliability_score"] - b["reliability_score"]) < 10
            )
            if similar:
                g.add_edge(a["supplier_id"], b["supplier_id"])
    return g


def main() -> None:
    logging.basicConfig(level=settings.log_level, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
    logger.info("Loading training data from %s", settings.data_path)
    df = pd.read_csv(settings.data_path)

    classes = set(df["risk_level"].unique().tolist())
    expected = {"Low", "Medium", "High"}
    if classes != expected:
        raise ValueError(f"Expected risk classes {sorted(expected)} but found {sorted(classes)}")

    x = df[FEATURE_COLUMNS]
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df["risk_level"])

    preprocessor = ColumnTransformer(
        [
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["country"]),
            ("num", StandardScaler(), [c for c in FEATURE_COLUMNS if c != "country"]),
        ]
    )

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)
    x_train_t = preprocessor.fit_transform(x_train)
    x_test_t = preprocessor.transform(x_test)

    model = XGBClassifier(
        n_estimators=160,
        max_depth=5,
        learning_rate=0.08,
        objective="multi:softprob",
        num_class=3,
        eval_metric="mlogloss",
        random_state=42,
    )
    model.fit(x_train_t, y_train)

    preds = model.predict(x_test_t)
    target_names = label_encoder.inverse_transform(sorted(set(y_test)))
    logger.info("Classification report:\n%s", classification_report(y_test, preds, target_names=target_names))
    logger.info("Confusion matrix:\n%s", confusion_matrix(y_test, preds))

    Path("models").mkdir(exist_ok=True)
    joblib.dump(preprocessor, settings.preprocessor_path)
    joblib.dump(model, settings.model_path)
    joblib.dump(label_encoder, settings.label_encoder_path)
    joblib.dump(build_graph(df), settings.graph_path)
    logger.info("Saved model artifacts to models/")


if __name__ == "__main__":
    main()
