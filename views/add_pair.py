import streamlit as st
from database import save_trade
from utils.instruments import get_mcx_master

@st.dialog("Create New Quant Spread")
def add_row_dialog():
    st.write("Select real metals and expiries directly from Dhan API:")
    
    # Fetch Master Data
    mcx_df = get_mcx_master()
    
    if mcx_df.empty:
        st.error("Failed to load metals from Dhan. Please check internet or API limits.")
        return
        
    # Get unique metals dynamically
    all_metals = sorted(mcx_df['BASE_SYMBOL'].dropna().unique())
    selected_metal = st.selectbox("Select Base Metal", all_metals)
    
    # Filter expiries specifically for the selected metal
    metal_data = mcx_df[mcx_df['BASE_SYMBOL'] == selected_metal]
    all_expiries = sorted(metal_data['SEM_EXPIRY_DATE'].dropna().unique())
    
    col1, col2 = st.columns(2)
    with col1:
        near_expiry = st.selectbox("Near Leg Expiry", all_expiries)
    with col2:
        far_expiry = st.selectbox("Far Leg Expiry", all_expiries)
        
    side = st.radio("Spread Direction", ["LONG", "SHORT"], horizontal=True)
    
    if st.button("Generate AI Trade", use_container_width=True):
        if near_expiry == far_expiry:
            st.error("Near and Far expiry cannot be the same!")
        else:
            # Pair ka format (Dashboard ke hisab se)
            pair_name = f"{selected_metal} {near_expiry}/{far_expiry}"
            save_trade(pair_name, side, "pending", 0.0, 0.0, 0.0)
            st.rerun()
