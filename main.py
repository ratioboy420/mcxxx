import streamlit as st
from database import init_db
from core.dhan_client import get_dhan_connection
from views.dashboard import render_live_dashboard

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dynamic MCX Quant Desk", layout="wide")

# --- INITIALIZE DATABASE ---
init_db()

# --- SIDEBAR LOGIN ---
with st.sidebar:
    st.header("🔑 API Login")
    client_id = st.text_input("Dhan Client ID", type="password")
    access_token = st.text_input("Access Token", type="password")
    
    if st.button("Connect"):
        if client_id and access_token:
            # Agar purana fail connection cache me hai, toh use hata do
            st.cache_resource.clear()
            
            # Connection try karo
            conn = get_dhan_connection(client_id, access_token)
            
            # Agar conn None nahi hai, tabhi Success dikhao!
            if conn is not None:
                st.session_state.dhan_conn = conn
                st.success("Connected to Dhan API!")
        else:
            st.warning("Please enter both credentials.")

# --- RENDER DASHBOARD ---
render_live_dashboard()
