"""Streamlit dashboard for cyber threat operations."""
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='SovereignAI SOC', layout='wide')
st.title('🇮🇳 SovereignAI Threat Operations')
st.sidebar.header('Navigation')
section = st.sidebar.radio('Select view', ['Overview', 'Threat History', 'Model Metrics'])
data = pd.read_csv('data/samples/network_logs.csv')
if section == 'Overview':
    st.metric('Critical Alerts', int((data['risk_score'] > 80).sum()))
    st.metric('Average Risk', round(float(data['risk_score'].mean()), 2))
    st.plotly_chart(px.histogram(data, x='risk_score', color='label', title='Risk Distribution'), use_container_width=True)
elif section == 'Threat History':
    st.dataframe(data, use_container_width=True)
else:
    st.info('Baseline model metrics are produced by scripts/train_model.py and can be registered in MLflow.')
