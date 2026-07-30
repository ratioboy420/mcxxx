import pandas as pd
import streamlit as st

@st.cache_data(ttl=3600)
def get_mcx_master():
    try:
        url = "https://images.dhan.co/api-data/api-scrip-master.csv"
        df = pd.read_csv(url, low_memory=False)
        
        mcx_df = df[df['SEM_EXM_EXCH_ID'] == 'MCX'].copy()
        mcx_df = mcx_df.dropna(subset=['SEM_CUSTOM_SYMBOL', 'SEM_EXPIRY_DATE'])
        mcx_df['BASE_SYMBOL'] = mcx_df['SEM_CUSTOM_SYMBOL'].str.extract(r'^([A-Za-z]+)')
        return mcx_df
    except Exception as e:
        st.error(f"Failed to fetch Scrip Master: {e}")
        return pd.DataFrame()

def get_security_token(base_symbol, expiry_date_str):
    """
    Finds the correct Dhan Security ID (SEM_SMST_SECURITY_ID) 
    by matching the Metal Name and Expiry Date.
    """
    mcx_master = get_mcx_master()
    if mcx_master.empty:
        return None
        
    try:
        # Convert the string date (e.g., '05-Oct-2026') to a date object
        target_date = pd.to_datetime(expiry_date_str).date()
        
        # Filter for the specific metal
        metal_df = mcx_master[mcx_master['BASE_SYMBOL'] == base_symbol].copy()
        
        # Match the expiry date
        metal_df['EXP_DATE_ONLY'] = pd.to_datetime(metal_df['SEM_EXPIRY_DATE']).dt.date
        match = metal_df[metal_df['EXP_DATE_ONLY'] == target_date]
        
        if not match.empty:
            # Dhan me SEM_SMST_SECURITY_ID hi wo token hota hai jisse Live Price milta hai
            return str(match.iloc[0]['SEM_SMST_SECURITY_ID'])
    except Exception:
        pass
        
    return None
