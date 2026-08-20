import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory of pages/ to sys.path to allow importing from utils package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.api_client import api_get
from utils.auth_state import show_auth_form

st.set_page_config(
    page_title="SalesGenie AI - Analytics",
    page_icon="📊",
    layout="wide"
)

# Auth Gate
if not show_auth_form():
    st.stop()

st.title("📊 Pipeline Analytics Dashboard")

# Fetch leads
leads = api_get("leads") or []

if leads:
    df = pd.DataFrame(leads)
    
    # KPIs from API
    kpi_data = api_get("kpis") or {}
    
    c1, c2, c3 = st.columns(3)
    c1.metric("📊 Total Active Leads", kpi_data.get("total_leads", len(leads)))
    c2.metric("💵 Est. Pipeline Value", f"${kpi_data.get('pipeline_value', len(leads)*15000):,}")
    c3.metric("🎯 Avg. AI Conversion Score", f"{kpi_data.get('avg_ai_score', 50.0):.1f}%")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏢 Leads by Industry")
        if "industry" in df.columns:
            ind_counts = df["industry"].value_counts().reset_index()
            ind_counts.columns = ["Industry", "Lead Count"]
            st.bar_chart(ind_counts.set_index("Industry"))
            
    with col2:
        st.subheader("📈 Leads by Pipeline Stage")
        if "stage" in df.columns:
            stage_counts = df["stage"].value_counts().reset_index()
            stage_counts.columns = ["Stage", "Lead Count"]
            st.bar_chart(stage_counts.set_index("Stage"))
            
    # AI Score Distribution
    st.subheader("🔥 AI Score Distribution")
    score_col = "ai_score" if "ai_score" in df.columns else "score"
    if score_col in df.columns:
        df_sorted = df.sort_values(by=score_col, ascending=False)
        st.line_chart(df_sorted.set_index("company")[score_col])
        
else:
    st.info("No opportunity data available. Please insert opportunities on the Home page.")
