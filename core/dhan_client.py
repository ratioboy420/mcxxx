import streamlit as st
from dhanhq import dhanhq

@st.cache_resource
def get_dhan_connection(client_id, access_token):
    """Establishes a persistent connection to Dhan API using stable version"""
    try:
        # Standard stable initialization
        conn = dhanhq(client_id, access_token)
        return conn
    except Exception as e:
        st.error(f"Dhan Connection Error: {e}")
        return None

def get_live_ltp(dhan_conn, security_id):
    """Fetches live price using the connection"""
    if dhan_conn:
        try:
            resp = dhan_conn.get_market_quote(exchange_segment='MCX', instrument_token=security_id)
            if resp and 'data' in resp and 'LTP' in resp['data']:
                return resp['data']['LTP']
            return 0.0
        except Exception:
            return 0.0
    return 0.0
