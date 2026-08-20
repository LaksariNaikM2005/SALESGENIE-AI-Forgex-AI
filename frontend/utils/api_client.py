import requests
import streamlit as st

API_BASE = "http://127.0.0.1:5000/api"

def get_token():
    return st.session_state.get("token")

def set_token(token):
    st.session_state["token"] = token

def clear_token():
    if "token" in st.session_state:
        del st.session_state["token"]

def get_headers():
    token = get_token()
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def api_get(endpoint):
    try:
        res = requests.get(f"{API_BASE.strip('/')}/{endpoint.strip('/')}", headers=get_headers())
        if res.status_code == 200:
            return res.json()
        return None
    except Exception as e:
        return None

def api_post(endpoint, data):
    try:
        res = requests.post(f"{API_BASE.strip('/')}/{endpoint.strip('/')}", json=data, headers=get_headers())
        return res
    except Exception as e:
        return None

def api_delete(endpoint):
    try:
        res = requests.delete(f"{API_BASE.strip('/')}/{endpoint.strip('/')}", headers=get_headers())
        return res
    except Exception as e:
        return None
