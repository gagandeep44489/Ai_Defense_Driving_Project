import pandas as pd
import plotly.express as px
import requests
import streamlit as st

API = "http://backend:8000/api/v1"

st.set_page_config(page_title="GeoSource AI", layout="wide")
st.title("GeoSource AI - Supplier Intelligence")

supplier_id = st.sidebar.text_input("Supplier ID", "SUP-0001")
headlines = st.sidebar.text_area("News Headlines (one per line)", "shipping delay at major port")

if st.button("Predict Risk"):
    payload = {
        "supplier": {
            "country": "US", "cost": 500, "delivery_time": 13,
            "reliability_score": 85, "defect_rate": 0.08, "delay_history": 4
        },
        "headlines": [h for h in headlines.split("\n") if h.strip()],
    }
    res = requests.post(f"{API}/predict-risk", json=payload, timeout=30)
    st.json(res.json())

if st.button("Get Recommendations"):
    res = requests.post(f"{API}/recommend", json={"supplier_id": supplier_id, "top_k": 3}, timeout=30)
    st.dataframe(pd.DataFrame(res.json().get("alternatives", [])))

if st.button("Graph Summary"):
    res = requests.get(f"{API}/graph-summary", timeout=30)
    s = res.json()
    st.metric("Nodes", s.get("nodes", 0))
    st.metric("Edges", s.get("edges", 0))
    fig = px.bar(x=["density"], y=[s.get("density", 0)])
    st.plotly_chart(fig, use_container_width=True)
