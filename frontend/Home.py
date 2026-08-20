import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory of Home.py to sys.path to allow importing from utils package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.api_client import api_get, api_post, api_delete
from utils.auth_state import show_auth_form

st.set_page_config(
    page_title="SalesGenie AI - Home",
    page_icon="🤖",
    layout="wide"
)

# Auth Gate
if not show_auth_form():
    st.stop()

st.title("🤖 SalesGenie AI Hub")
st.markdown("Welcome to the **SalesGenie AI** (Forgex AI) lead prediction and outreach dashboard. Use the sidebar to navigate to the analytical tools.")

# Fetch Leads
leads = api_get("leads") or []

# Stats Cards
if leads:
    df = pd.DataFrame(leads)
    
    # Calculate KPIs
    total_leads = len(df)
    pipeline_value = total_leads * 15000 # Fallback
    avg_score = df["ai_score"].mean() if "ai_score" in df else 0.0
    
    # Render KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("📈 Total Leads", total_leads)
    c2.metric("💰 Est. Pipeline Value", f"${pipeline_value:,}")
    c3.metric("🔥 Avg. AI Score", f"{avg_score:.1f}%")
    
    # Show active leads table
    st.subheader("📋 Active Sales Pipeline")
    # Dynamically select present columns
    show_cols = [c for c in ["id", "company", "industry", "contact_person", "stage", "ai_score", "score"] if c in df.columns]
    st.dataframe(
        df[show_cols],
        use_container_width=True
    )
else:
    st.info("No active leads found in the pipeline database. Create a new lead below.")

# Lead Insertion Form
st.subheader("➕ Add New Opportunity")
with st.form("new_lead_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    company = col1.text_input("Company Name")
    contact = col1.text_input("Contact Person")
    industry = col2.text_input("Industry")
    stage = col2.selectbox("Pipeline Stage", ["New Lead", "Qualified", "Proposal", "Negotiation", "Closed Won"])
    score = st.slider("Initial Score (0-100)", 0, 100, 50)
    
    submit = st.form_submit_button("Add Lead Opportunity")
    if submit:
        if company and contact:
            res = api_post("leads", {
                "company": company,
                "contact_person": contact,
                "industry": industry or "Unknown",
                "stage": stage,
                "score": score
            })
            if res and res.status_code == 201:
                st.success("Lead created successfully!")
                st.rerun()
            else:
                st.error("Failed to create lead.")
        else:
            st.warning("Please fill in Company Name and Contact Person.")
