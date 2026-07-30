import streamlit as st
from dhanhq import dhanhq  # Dhan library import activated

@st.cache_resource
def get_dhan_connection(client_id, access_token):
    """Establishes a persistent connection to Dhan API"""
    try:
        # Actual Dhan API Connection
        return dhanhq(client_id, access_token)
    except Exception as e:
        st.error(f"Dhan Connection Error: {e}")
        return None

def get_live_ltp(dhan_conn, security_id):
    """Fetches live price using the connection"""
    if dhan_conn:
        try:
            # Actual API call to fetch Live Traded Price (LTP)
            resp = dhan_conn.get_market_quote(exchange_segment='MCX', instrument_token=security_id)
            
            # Extracting the LTP from the response dictionary
            if resp and 'data' in resp and 'LTP' in resp['data']:
                return resp['data']['LTP']
            return 0.0
        except Exception as e:
            # Silently handle errors so the dashboard doesn't crash on a missed tick
            return 0.0
    return 0.0
