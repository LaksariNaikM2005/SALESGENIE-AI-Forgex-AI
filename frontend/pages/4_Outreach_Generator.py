import streamlit as st
import sys
import os

# Add parent directory of pages/ to sys.path to allow importing from utils package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.api_client import api_post
from utils.auth_state import show_auth_form

st.set_page_config(
    page_title="SalesGenie AI - Outreach",
    page_icon="✉️",
    layout="wide"
)

# Auth Gate
if not show_auth_form():
    st.stop()

st.title("✉️ AI Outreach Email Generator")
st.markdown("Compose contextual outbound email messages tailored to specific prospects using AI insights.")

col1, col2 = st.columns(2)
with col1:
    prospect_name = st.text_input("Prospect Name", placeholder="e.g. Jane Doe")
    company_name = st.text_input("Company Name", placeholder="e.g. Acme Corp")
    value_prop = st.text_area("Value Proposition / Tone Focus", placeholder="e.g. Mention 20% discount or CRM automation efficiency benefits")
    
with col2:
    st.write("") # Padding
    
if st.button("✨ Generate AI Outreach Email", use_container_width=True):
    if prospect_name and company_name:
        res = api_post("outreach", {
            "name": prospect_name,
            "company": company_name,
            "details": value_prop
        })
        if res and res.status_code == 200:
            data = res.json()
            generated_text = data.get("generated_email", "")
            
            st.subheader("📝 Generated Outreach Draft")
            st.text_area("Email Content", generated_text, height=200)
            st.success("Draft created! You can copy and customize it above.")
        else:
            st.error("Failed to generate email draft. Backend server might be offline.")
    else:
        st.warning("Please fill in both Prospect Name and Company Name fields.")
