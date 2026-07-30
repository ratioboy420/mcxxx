import streamlit as st
from dhanhq import dhanhq

@st.cache_resource
def get_dhan_connection(client_id, access_token):
    """Establishes a persistent connection to Dhan API adapting to any SDK version"""
    try:
        # Attempt 1: Naye Dhan SDK version me shayad sirf access_token chahiye
        try:
            conn = dhanhq(access_token=access_token)
            return conn
        except TypeError:
            pass
        
        # Attempt 2: Agar library 'clientcode' naam expect kar rahi ho
        try:
            conn = dhanhq(clientcode=client_id, access_token=access_token)
            return conn
        except TypeError:
            pass

        # Attempt 3: Purana standard tarika (Positional arguments)
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
