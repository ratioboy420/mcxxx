import streamlit as st
import pandas as pd
from database import save_trade
from utils.instruments import get_mcx_master
from ai.quant_ai import get_ai_trade_decision

@st.dialog("🤖 AI Strategy Leg Generator")
def add_row_dialog():
    st.write("Select Metal and Expiries. AI will decide the direction.")
    
    mcx_master = get_mcx_master()
    if mcx_master.empty:
        st.error("Scrip master data not available.")
        return

    all_metals = sorted(mcx_master['BASE_SYMBOL'].dropna().unique().tolist())
    selected_metal = st.selectbox("1. Select Base Metal", all_metals)
    
    metal_df = mcx_master[mcx_master['BASE_SYMBOL'] == selected_metal]
    metal_df['EXPIRY_DATETIME'] = pd.to_datetime(metal_df['SEM_EXPIRY_DATE'])
    active_expiries = sorted(metal_df['EXPIRY_DATETIME'].dt.date.unique().tolist())
    expiry_options = [exp.strftime('%d-%b-%Y') for exp in active_expiries]
    
    if len(expiry_options) < 2:
        st.warning(f"Not enough expiries found for {selected_metal}.")
        return
        
    col1, col2 = st.columns(2)
    with col1:
        near_expiry = st.selectbox("2. Near Expiry (Leg 1)", expiry_options, index=0)
    with col2:
        far_expiry = st.selectbox("3. Far Expiry (Leg 2)", expiry_options, index=1)
        
    if st.button("🧠 Analyze with AI & Add to Desk", type="primary"):
        with st.spinner("Analyzing Z-Score, RSI, and Open Interest..."):
            
            # Fetch AI Decision
            side, reason = get_ai_trade_decision(selected_metal, near_expiry, far_expiry)
            pair_name = f"{selected_metal} {near_expiry}/{far_expiry}"
            
            # Save trade to SQLite database
            save_trade(pair_name, side, "pending", 0.0, 0.0, 0.0)
            
            st.success(f"Trade Approved by AI: {side}")
            st.info(reason)
            st.caption("Closing dialog... Dashboard will update automatically in a few seconds.")
            # Note: Removed st.rerun() here to permanently fix the Fragment Error in your logs.
