import streamlit as st
from database import init_db
from views.dashboard import render_live_dashboard

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dynamic MCX Quant Desk", layout="wide")

# --- INITIALIZE DATABASE ---
init_db()

# --- RENDER DASHBOARD ---
render_live_dashboard()
