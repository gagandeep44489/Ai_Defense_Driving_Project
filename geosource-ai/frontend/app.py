"""Streamlit dashboard for GeoSource AI advanced intelligence."""
from __future__ import annotations

from pathlib import Path
import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

from backend.graph_model import load_graph_artifacts


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "data" / "suppliers.csv"
API_BASE_URL = "http://127.0.0.1:8000"


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def draw_local_graph(selected_supplier: str) -> None:
    artifacts = load_graph_artifacts()
    g = artifacts.graph
    sub_nodes = {selected_supplier}
    if selected_supplier in g:
        sub_nodes.update(g.neighbors(selected_supplier))
    subgraph = g.subgraph(sub_nodes)

    fig, ax = plt.subplots(figsize=(8, 5))
    pos = nx.spring_layout(subgraph, seed=42)
    colors = ["#e74c3c" if n == selected_supplier else "#3498db" for n in subgraph.nodes]
    nx.draw_networkx(subgraph, pos=pos, node_color=colors, with_labels=True, node_size=450, font_size=8, ax=ax)
    ax.set_title("Supplier Local Graph (selected in red)")
    ax.axis("off")
    st.pyplot(fig)


def main() -> None:
    st.set_page_config(page_title="GeoSource AI Dashboard", layout="wide")
    st.title("🌍 GeoSource AI — Advanced Supply Intelligence")

    df = load_data()
    supplier_id = st.selectbox("Select supplier", options=df["supplier_id"].tolist())
    row = df[df["supplier_id"] == supplier_id].iloc[0]

    st.subheader("External News Signals")
    default_headlines = (
        "Factory strike impacts logistics in supplier region\n"
        "Supplier announces major quality improvement program\n"
        "Port congestion causes shipment delay"
    )
    headlines_text = st.text_area("Enter one headline per line", value=default_headlines, height=100)
    headlines = [line.strip() for line in headlines_text.splitlines() if line.strip()]

    payload = {
        "country": str(row["country"]),
        "cost": float(row["cost"]),
        "delivery_time": float(row["delivery_time"]),
        "reliability_score": float(row["reliability_score"]),
        "defect_rate": float(row["defect_rate"]),
        "delay_history": int(row["delay_history"]),
        "headlines": headlines,
    }

    left, right = st.columns(2)
    with left:
        st.subheader("Supplier Snapshot")
        st.json(payload)

    with right:
        st.subheader("Risk Prediction")
        try:
            response = requests.post(f"{API_BASE_URL}/predict-risk", json=payload, timeout=12)
            response.raise_for_status()
            risk_data = response.json()
            c1, c2, c3 = st.columns(3)
            c1.metric("Model Risk", risk_data["model_risk"])
            c2.metric("Final Risk", risk_data["final_risk"])
            c3.metric("Combined Score", f"{risk_data['combined_score']:.2f}")
            st.caption(f"News summary: {risk_data['news_summary']}")

            st.subheader("Risk Explanation (Top Features)")
            explain_df = pd.DataFrame(risk_data["feature_explanations"]).head(8)
            st.bar_chart(explain_df.set_index("feature")["impact"])
        except Exception:
            st.warning("API unavailable. Start FastAPI backend to compute risk and explanations.")
            risk_data = None

    st.subheader("Top 3 Alternative Suppliers")
    try:
        rec_response = requests.post(
            f"{API_BASE_URL}/recommend", json={"supplier_id": supplier_id}, timeout=10
        )
        rec_response.raise_for_status()
        alternatives = pd.DataFrame(rec_response.json()["alternatives"])
        st.dataframe(alternatives, use_container_width=True)

        if not alternatives.empty:
            st.markdown("**Highlighted picks:** " + ", ".join(f"`{sid}`" for sid in alternatives["supplier_id"].tolist()))
    except Exception:
        st.warning("API unavailable. Start FastAPI backend to see recommendations.")

    st.subheader("Supplier Graph View")
    try:
        draw_local_graph(supplier_id)
    except Exception:
        st.info("Graph visualization unavailable until dependencies are installed.")


if __name__ == "__main__":
    main()
