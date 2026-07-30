import streamlit as st
import pandas as pd
import sqlite3
from views.add_pair import add_row_dialog
from core.dhan_client import get_live_ltp, get_historical_prices
from core.quant_math import calculate_advanced_spread
from utils.instruments import get_security_token
from database import delete_trade

@st.fragment(run_every=5)
def render_live_dashboard():
    st.subheader("📊 Live Pair Spread Desk")
    
    dhan_conn = st.session_state.get('dhan_conn')
    
    col1, col2 = st.columns([8, 2])
    with col1:
        if dhan_conn:
            st.success("🟢 Real-time Market & Historical Data Active")
        else:
            st.warning("⚠️ Dhan API Not Connected.")
    with col2:
        if st.button("➕ AI Add Row", use_container_width=True):
            add_row_dialog()
            
    st.divider()

    try:
        conn = sqlite3.connect('mcx_trades.db')
        df = pd.read_sql_query("SELECT * FROM trades", conn)
        conn.close()
        
        if df.empty:
            st.info("No active trades. Click 'AI Add Row' to generate a spread.")
            return

        for index, row in df.iterrows():
            with st.container():
                c1, c2, c3, c4, c5 = st.columns([2.5, 2, 2, 2, 1.5])
                
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
                    
                    if st.button("🗑️ Delete", key=f"del_{row['id']}"):
                        delete_trade(row['id'])
                        st.rerun()
                
                # Fetch Tokens
                near_token = get_security_token(metal, near_exp)
                far_token = get_security_token(metal, far_exp)
                
                # Fetch Live Prices
                near_live = get_live_ltp(dhan_conn, near_token) if near_token else 0.0
                far_live = get_live_ltp(dhan_conn, far_token) if far_token else 0.0
                
                # Fetch Historical Prices (Background execution)
                near_hist = get_historical_prices(dhan_conn, near_token)
                far_hist = get_historical_prices(dhan_conn, far_token)
                
                # Create Historical Spread List (Matching lists dynamically)
                historical_spreads = []
                if near_hist and far_hist:
                    min_len = min(len(near_hist), len(far_hist))
                    near_hist = near_hist[-min_len:]
                    far_hist = far_hist[-min_len:]
                    historical_spreads = [n - f for n, f in zip(near_hist, far_hist)]
                
                # Run the Real Math Engine!
                live_spread, calc_target, calc_sl, z_score, rsi = calculate_advanced_spread(
                    near_live, far_live, row['side'], historical_spreads
                )
                
                with c2:
                    if near_live == 0.0 or far_live == 0.0:
                        st.error("Offline")
                    else:
                        st.metric(label=f"Spread ({row['side']})", value=f"₹{live_spread:,.2f}")
                
                with c3:
                    st.metric(label="Target", value=f"₹{calc_target:,.2f}")
                    st.metric(label="Stop Loss", value=f"₹{calc_sl:,.2f}")
                    
                with c4:
                    # RENDER Z-SCORE AND RSI
                    z_color = "red" if abs(z_score) > 1.5 else "green"
                    st.markdown(f"**Z-Score:** <span style='color:{z_color}'>{z_score}</span>", unsafe_allow_html=True)
                    st.markdown(f"**RSI (14):** {rsi}")
                
                with c5:
                    pnl = 0 
                    st.metric(label="Live P&L", value=f"₹{pnl}")
                
                st.markdown("---")

    except Exception as e:
        st.error(f"Error loading dashboard: {e}")
