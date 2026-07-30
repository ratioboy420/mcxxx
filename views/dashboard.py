import streamlit as st
import pandas as pd
import sqlite3
from views.add_pair import add_row_dialog
from core.dhan_client import get_live_ltp
from core.quant_math import calculate_spread_math
from utils.instruments import get_security_token

@st.fragment(run_every=5)
def render_live_dashboard():
    st.subheader("📊 Live Pair Spread Desk")
    
    dhan_conn = st.session_state.get('dhan_conn')
    
    # 1. HEADER BUTTONS
    col1, col2 = st.columns([8, 2])
    with col1:
        if dhan_conn:
            st.success("🟢 Real-time Market Data Active")
        else:
            st.warning("⚠️ Dhan API Not Connected. Please login from the sidebar.")
    with col2:
        if st.button("➕ AI Add Row", use_container_width=True):
            add_row_dialog()
            
    st.divider()

    # 2. LOAD TRADES FROM DB
    try:
        conn = sqlite3.connect('mcx_trades.db')
        df = pd.read_sql_query("SELECT * FROM trades", conn)
        conn.close()
        
        if df.empty:
            st.info("No active trades. Click 'AI Add Row' to generate a spread.")
            return

        # 3. RENDER TRADES WITH REAL DYNAMIC DATA
        for index, row in df.iterrows():
            with st.container():
                c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
                
                # Parsing string: "GOLD 05-Oct-2026/04-Dec-2026"
                try:
                    pair_parts = row['pair'].split(' ')
                    metal = pair_parts[0]
                    expiries = pair_parts[1].split('/')
                    near_exp = expiries[0]
                    far_exp = expiries[1]
                except Exception:
                    metal, near_exp, far_exp = "", "", ""
                
                with c1:
                    st.markdown(f"### {row['pair']}")
                    st.caption(f"Status: **{row['status']}** | Opened: {row['open_time']}")
                
                with c2:
                    # --- NO MORE MANUAL DATA: Fetching Real Dynamic Tokens ---
                    near_token = get_security_token(metal, near_exp)
                    far_token = get_security_token(metal, far_exp)
                    
                    near_live = get_live_ltp(dhan_conn, near_token) if near_token else 0.0
                    far_live = get_live_ltp(dhan_conn, far_token) if far_token else 0.0
                    
                    # Mathematical Calculation
                    live_spread, calc_target, calc_sl = calculate_spread_math(near_live, far_live, row['side'])
                    
                    if near_live == 0.0 or far_live == 0.0:
                        st.error("Market Data Offline")
                    else:
                        st.metric(label=f"Live Spread ({row['side']})", value=f"₹{live_spread:,.2f}")
                
                with c3:
                    st.metric(label="Target", value=f"₹{calc_target:,.2f}")
                    st.metric(label="Stop Loss", value=f"₹{calc_sl:,.2f}")
                    
                with c4:
                    # Future integration logic for P&L based on entry price
                    pnl = 0 
                    st.metric(label="Live P&L", value=f"₹{pnl}")
                
                st.markdown("---")

    except Exception as e:
        st.error(f"Error loading dashboard: {e}")
