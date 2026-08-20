import streamlit as st
import sys
import os

# Add parent directory of pages/ to sys.path to allow importing from utils package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.api_client import api_get
from utils.auth_state import show_auth_form

st.set_page_config(
    page_title="SalesGenie AI - Sales Intel",
    page_icon="🔍",
    layout="wide"
)

# Auth Gate
if not show_auth_form():
    st.stop()

st.title("🔍 Sales Intelligence & Intent Insights")

# Fetch leads
leads = api_get("leads") or []

if leads:
    lead_opts = {f"{l['company']} (Contact: {l['contact_person']})": l for l in leads}
    selected_option = st.selectbox("Select Active Lead Opportunity", list(lead_opts.keys()))
    
    if selected_option:
        lead_data = lead_opts[selected_option]
        lead_id = lead_data.get("id")
        
        # Call features endpoints
        company_intel = api_get(f"company-details/{lead_id}") or {}
        ai_insights = api_get(f"ai-lead-intelligence/{lead_id}") or {}
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏢 Company Firmographic Intelligence")
            st.write(f"**Company:** {lead_data.get('company')}")
            st.write(f"**Industry Segment:** {lead_data.get('industry')}")
            st.info(f"💡 **Intel Digest:** {company_intel.get('intel', 'No recent intel updates found.')}")
            
        with col2:
            st.subheader("🎯 Lead Intent & Insights")
            st.write(f"**Contact Person:** {lead_data.get('contact_person')}")
            st.write(f"**AI Score:** {lead_data.get('ai_score', lead_data.get('score', 0))}%")
            
            insights_list = ai_insights.get("insights", [])
            if insights_list:
                for ins in insights_list:
                    st.write(f"✔️ {ins}")
            else:
                st.write("No specific intent flags detected for this contact yet.")
else:
    st.info("Please add opportunity leads on the Home page first.")
