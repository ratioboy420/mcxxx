import streamlit as st
import pandas as pd
import sqlite3
from views.add_pair import add_row_dialog
from core.dhan_client import get_live_ltp
from core.quant_math import calculate_spread_math

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

        # 3. RENDER TRADES AS DYNAMIC BOXES (CARDS)
        for index, row in df.iterrows():
            # Create a card-like container for each pair
            with st.container():
                c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
                
                with c1:
                    st.markdown(f"### {row['pair']}")
                    st.caption(f"Status: **{row['status']}** | Opened: {row['open_time']}")
                
                with c2:
                    # Simulated Live Fetching & Math (Will be replaced with dynamic tokens next)
                    # Yahan Near aur Far leg ka live price aayega
                    near_live = 72500.0  
                    far_live = 73000.0   
                    
                    live_spread, calc_target, calc_sl = calculate_spread_math(near_live, far_live, row['side'])
                    
                    st.metric(label=f"Live Spread ({row['side']})", value=f"₹{live_spread}")
                
                with c3:
                    st.metric(label="Target", value=f"₹{calc_target}")
                    st.metric(label="Stop Loss", value=f"₹{calc_sl}")
                    
                with c4:
                    # Dummy PnL logic for now
                    pnl = 0 
                    st.metric(label="Live P&L", value=f"₹{pnl}")
                
                st.markdown("---") # Box divider

    except Exception as e:
        st.error(f"Error loading dashboard: {e}")
