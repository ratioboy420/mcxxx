import streamlit as st
import pandas as pd
import sqlite3
from views.add_pair import add_row_dialog
from core.dhan_client import get_live_ltp

@st.fragment(run_every=5)
def render_live_dashboard():
    st.subheader("📊 Live Pair Spread Desk")
    
    # 1. LIVE TICKER
    dhan_conn = st.session_state.get('dhan_conn')
    live_rates_display = "Live MCX Rates: "
    
    if dhan_conn:
        # Example Security IDs for Gold and Silver
        gold_price = get_live_ltp(dhan_conn, "426176") 
        silver_price = get_live_ltp(dhan_conn, "426211") 
        live_rates_display += f"GOLD **₹{gold_price}** | SILVER **₹{silver_price}**"
    else:
        live_rates_display += "⚠️ Dhan API Not Connected. (Showing placeholders: GOLD ₹72,450 | SILVER ₹89,120)"
        
    col1, col2 = st.columns([8, 2])
    with col1:
        st.markdown(live_rates_display)
    with col2:
        if st.button("➕ AI Add Row", use_container_width=True):
            add_row_dialog()
            
    # 2. LOAD DB & RENDER TABLE
    try:
        conn = sqlite3.connect('mcx_trades.db')
        query = "SELECT pair as Pair, side as Side, status as Status, open_time as Opened, entry_price as Entry, target as Target, stop_loss as Stop, pnl as 'P/L' FROM trades"
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No active trades. Click 'AI Add Row' to generate a spread.")
            
    except Exception as e:
        st.error(f"Error loading database: {e}")
