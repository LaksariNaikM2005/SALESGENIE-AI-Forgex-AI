import streamlit as st
from utils.api_client import api_post, set_token, clear_token, get_token

def login_user(username, password):
    res = api_post("auth/login", {"username": username, "password": password})
    if res and res.status_code == 200:
        data = res.json()
        set_token(data.get("access_token"))
        st.session_state["username"] = username
        return True
    return False

def register_user(username, password):
    res = api_post("auth/register", {"username": username, "password": password})
    if res and res.status_code == 201:
        return True
    return False

def logout_user():
    clear_token()
    if "username" in st.session_state:
        del st.session_state["username"]
    st.rerun()

def show_auth_form():
    if "username" in st.session_state:
        st.sidebar.write(f"Logged in as: **{st.session_state['username']}**")
        if st.sidebar.button("Logout"):
            logout_user()
        return True
        
    st.title("🔐 Authentication Required")
    st.info("Please login or register to access the SalesGenie AI platform.")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        u = st.text_input("Username", key="login_u")
        p = st.text_input("Password", type="password", key="login_p")
        if st.button("Login", key="btn_login"):
            if login_user(u, p):
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials.")
                
    with tab2:
        reg_u = st.text_input("Username", key="reg_u")
        reg_p = st.text_input("Password", type="password", key="reg_p")
        if st.button("Register", key="btn_reg"):
            if register_user(reg_u, reg_p):
                st.success("Registered successfully! You can now login.")
            else:
                st.error("Failed to register. Username might exist.")
    return False
