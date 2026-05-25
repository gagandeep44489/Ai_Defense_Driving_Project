"""Streamlit dashboard for GeoSource AI."""
from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

API_BASE_URL = "http://backend:8000/api/v1"
REQUEST_TIMEOUT = 30


@st.cache_data(ttl=30)
def get_graph_summary() -> dict[str, Any]:
    response = requests.get(f"{API_BASE_URL}/graph-summary", timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()


def post_predict(payload: dict[str, Any]) -> dict[str, Any]:
    response = requests.post(f"{API_BASE_URL}/predict-risk", json=payload, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()


def post_recommendations(payload: dict[str, Any]) -> dict[str, Any]:
    response = requests.post(f"{API_BASE_URL}/recommend", json=payload, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()


def render_sidebar() -> dict[str, Any]:
    st.sidebar.title("GeoSource AI")
    st.sidebar.caption("Supplier Intelligence Dashboard")

    page = st.sidebar.radio(
        "Navigation",
        options=["Risk Prediction", "Recommendations", "Graph Intelligence"],
    )

    st.sidebar.subheader("Supplier Inputs")
    supplier_id = st.sidebar.text_input("Supplier ID", "SUP-0001")
    country = st.sidebar.selectbox("Country", ["US", "DE", "JP", "MX", "CN", "KR", "IN"], index=0)
    cost = st.sidebar.slider("Cost", min_value=150.0, max_value=1100.0, value=500.0, step=10.0)
    delivery_time = st.sidebar.slider("Delivery Time (days)", min_value=3.0, max_value=40.0, value=14.0, step=1.0)
    reliability_score = st.sidebar.slider("Reliability Score", min_value=0.0, max_value=100.0, value=85.0, step=1.0)
    defect_rate = st.sidebar.slider("Defect Rate", min_value=0.0, max_value=1.0, value=0.08, step=0.01)
    delay_history = st.sidebar.slider("Delay History", min_value=0, max_value=25, value=4, step=1)
    top_k = st.sidebar.slider("Top-K Recommendations", min_value=1, max_value=10, value=3, step=1)

    headlines_text = st.sidebar.text_area(
        "News Headlines (one per line)",
        "shipping delay at major port\nsupplier operations improved in asia",
        height=120,
    )
    headlines = [line.strip() for line in headlines_text.splitlines() if line.strip()]

    return {
        "page": page,
        "supplier_id": supplier_id,
        "supplier": {
            "supplier_id": supplier_id,
            "country": country,
            "cost": cost,
            "delivery_time": delivery_time,
            "reliability_score": reliability_score,
            "defect_rate": defect_rate,
            "delay_history": delay_history,
        },
        "top_k": top_k,
        "headlines": headlines,
    }


def render_risk_prediction_ui(state: dict[str, Any]) -> None:
    st.header("Risk Prediction")
    st.write("Predict supplier operational risk and review explainability signals.")

    if st.button("Run Risk Prediction", type="primary", use_container_width=True):
        payload = {"supplier": state["supplier"], "headlines": state["headlines"]}
        with st.spinner("Running risk inference..."):
            try:
                result = post_predict(payload)
            except requests.RequestException as exc:
                st.error(f"Prediction request failed: {exc}")
                return

        col1, col2, col3 = st.columns(3)
        col1.metric("Risk Level", result.get("risk_level", "N/A"))
        col2.metric("Confidence", f"{result.get('confidence', 0.0):.2%}")
        col3.metric("Final Risk Score", f"{result.get('risk_score', 0.0):.2f}")

        signal = result.get("nlp_signal", {})
        st.info(
            f"NLP Signal: sentiment={signal.get('sentiment', 0):.2f}, "
            f"adjustment={signal.get('risk_adjustment', 0):.2f} | {signal.get('summary', '')}"
        )

        explanation = result.get("explanation", {})
        importance_values = explanation.get("importance_values", [])
        if importance_values:
            importance_df = pd.DataFrame(importance_values)
            fig = px.bar(
                importance_df,
                x="feature",
                y="value",
                title="SHAP-style Feature Importance",
                color="value",
                color_continuous_scale="Blues",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No explainability data available.")


def render_recommendations_ui(state: dict[str, Any]) -> None:
    st.header("Supplier Recommendations")
    st.write("Find alternative suppliers using graph + operational similarity.")

    if st.button("Get Recommendations", type="primary", use_container_width=True):
        payload = {"supplier_id": state["supplier_id"], "top_k": state["top_k"]}
        with st.spinner("Calculating alternatives..."):
            try:
                result = post_recommendations(payload)
            except requests.RequestException as exc:
                st.error(f"Recommendation request failed: {exc}")
                return

        alternatives = result.get("alternatives", [])
        if not alternatives:
            st.warning("No recommendations returned by API.")
            return

        rec_df = pd.DataFrame(alternatives)
        st.dataframe(rec_df, use_container_width=True)
        fig = px.bar(rec_df, x="supplier_id", y="score", color="risk_level", title="Top Supplier Alternatives")
        st.plotly_chart(fig, use_container_width=True)


def render_graph_ui() -> None:
    st.header("Graph Intelligence")
    st.write("View graph density and network scale metrics.")

    if st.button("Refresh Graph Metrics", type="primary", use_container_width=True):
        with st.spinner("Loading graph summary..."):
            try:
                summary = get_graph_summary()
            except requests.RequestException as exc:
                st.error(f"Graph summary request failed: {exc}")
                return

        c1, c2, c3 = st.columns(3)
        c1.metric("Nodes", summary.get("nodes", 0))
        c2.metric("Edges", summary.get("edges", 0))
        c3.metric("Density", f"{summary.get('density', 0.0):.4f}")

        chart_df = pd.DataFrame(
            {
                "metric": ["nodes", "edges", "density"],
                "value": [summary.get("nodes", 0), summary.get("edges", 0), summary.get("density", 0.0)],
            }
        )
        fig = px.bar(chart_df, x="metric", y="value", title="Supplier Graph Summary")
        st.plotly_chart(fig, use_container_width=True)


def main() -> None:
    st.set_page_config(page_title="GeoSource AI", page_icon="🚗", layout="wide")
    st.title("GeoSource AI Dashboard")
    st.caption("AI-powered supplier intelligence for automotive supply chains")

    state = render_sidebar()

    if state["page"] == "Risk Prediction":
        render_risk_prediction_ui(state)
    elif state["page"] == "Recommendations":
        render_recommendations_ui(state)
    else:
        render_graph_ui()


if __name__ == "__main__":
    main()
