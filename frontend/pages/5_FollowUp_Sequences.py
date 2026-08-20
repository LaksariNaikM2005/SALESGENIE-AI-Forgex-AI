import streamlit as st
import sys
import os

# Add parent directory of pages/ to sys.path to allow importing from utils package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.api_client import api_get
from utils.auth_state import show_auth_form

st.set_page_config(
    page_title="SalesGenie AI - Follow-ups",
    page_icon="📅",
    layout="wide"
)

# Auth Gate
if not show_auth_form():
    st.stop()

st.title("📅 Follow-up Campaigns & Sequences")
st.markdown("Track and trigger automated outreach follow-up schedules.")

# Fetch followups
followups = api_get("follow-ups") or []

if followups:
    st.subheader("📋 Active Outreach Sequences")
    for f in followups:
        col1, col2, col3 = st.columns([1, 2, 1])
        col1.write(f"**Lead ID:** {f.get('lead_id')}")
        col2.write(f"📝 **Action:** {f.get('action')}")
        col3.write(f"📅 **Due:** {f.get('due')}")
        st.markdown("---")
else:
    st.info("No active follow-up sequences found.")
