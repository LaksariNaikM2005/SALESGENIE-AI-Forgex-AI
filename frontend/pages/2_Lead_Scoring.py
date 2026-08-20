import streamlit as st
import sys
import os

# Add parent directory of pages/ to sys.path to allow importing from utils package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.api_client import api_post
from utils.auth_state import show_auth_form

st.set_page_config(
    page_title="SalesGenie AI - Lead Scoring",
    page_icon="🧠",
    layout="wide"
)

# Auth Gate
if not show_auth_form():
    st.stop()

st.title("🧠 Predictive ML Lead Scoring Engine")
st.markdown("Use our Random Forest model to calculate lead conversion probability based on client engagement metrics.")

st.subheader("📝 Input Engagement Metrics")

col1, col2 = st.columns(2)
with col1:
    emails = st.number_input("Outbound Emails Opened / Replied", min_value=0, max_value=200, value=5, step=1)
    visits = st.number_input("Website Sessions / Visits", min_value=0, max_value=500, value=10, step=1)
with col2:
    st.write("") # Padding
    st.write("") # Padding
    demo_requested = st.checkbox("Product Demo Requested / Attended", value=False)

if st.button("📊 Calculate Conversion Probability", use_container_width=True):
    # Call Flask prediction endpoint
    res = api_post("predict", {
        "emails": emails,
        "visits": visits,
        "demo": demo_requested
    })
    
    if res and res.status_code == 200:
        data = res.json()
        score = data.get("score", 0.0)
        category = data.get("category", "Cold")
        
        # Display Result Card
        st.success("Analysis Completed!")
        c1, c2 = st.columns(2)
        
        # Choose badge colors based on category
        cat_colors = {
            "Hot": "🔴 Hot Lead",
            "Warm": "🟡 Warm Lead",
            "Cold": "🔵 Cold Lead"
        }
        
        c1.metric("🔮 AI Probability Score", f"{score:.1f}%")
        c2.metric("🏷️ Lead Classification Segment", cat_colors.get(category, f" {category}"))
        
        # Visual Progress Bar
        st.progress(score / 100.0)
    else:
        st.error("Failed to connect to the backend ML model endpoint. Ensure the backend is online.")
