import pandas as pd
import streamlit as st

@st.cache_data(ttl=3600)  # Caches the file for 1 hour to prevent API bans
def get_mcx_master():
    try:
        url = "https://images.dhan.co/api-data/api-scrip-master.csv"
        df = pd.read_csv(url, low_memory=False)
        
        # Filter for MCX and remove bad data
        mcx_df = df[df['SEM_EXM_EXCH_ID'] == 'MCX'].copy()
        mcx_df = mcx_df.dropna(subset=['SEM_CUSTOM_SYMBOL', 'SEM_EXPIRY_DATE'])
        
        # Create BASE_SYMBOL (e.g., 'GOLD' from 'GOLD 05OCT2026')
        mcx_df['BASE_SYMBOL'] = mcx_df['SEM_CUSTOM_SYMBOL'].str.extract(r'^([A-Za-z]+)')
        return mcx_df
    except Exception as e:
        st.error(f"Failed to fetch Scrip Master: {e}")
        return pd.DataFrame()
