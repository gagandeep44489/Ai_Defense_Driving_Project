import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBClassifier
import networkx as nx

from backend.core.config import settings


def build_graph(df: pd.DataFrame) -> nx.Graph:
    g = nx.Graph()
    for _, row in df.iterrows():
        g.add_node(row.supplier_id, country=row.country, risk=row.risk_level)
    rows = df.to_dict("records")
    for i, a in enumerate(rows):
        for b in rows[i + 1 :]:
            similar = a["country"] == b["country"] or abs(a["cost"] - b["cost"]) < 100 or abs(a["reliability_score"] - b["reliability_score"]) < 10
            if similar:
                g.add_edge(a["supplier_id"], b["supplier_id"])
    return g


def main() -> None:
    df = pd.read_csv(settings.data_path)
    y = df["risk_level"]
    x = df[["country", "cost", "delivery_time", "reliability_score", "defect_rate", "delay_history"]]
    cat = ["country"]
    num = [c for c in x.columns if c not in cat]
    pre = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat),
        ("num", StandardScaler(), num),
    ])
    model = XGBClassifier(n_estimators=120, max_depth=4, learning_rate=0.08, objective="multi:softprob", eval_metric="mlogloss")
    pipe = Pipeline([("pre", pre), ("model", model)])
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)
    pipe.fit(x_train, y_train)
    print(classification_report(y_test, pipe.predict(x_test)))
    joblib.dump(pipe.named_steps["pre"], settings.preprocessor_path)
    joblib.dump(pipe.named_steps["model"], settings.model_path)
    joblib.dump(build_graph(df), settings.graph_path)


if __name__ == "__main__":
    main()
