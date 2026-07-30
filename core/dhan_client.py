import streamlit as st
# from dhanhq import dhanhq  # Uncomment this when you put real API keys

@st.cache_resource
def get_dhan_connection(client_id, access_token):
    """Establishes a persistent connection to Dhan API"""
    try:
        # return dhanhq(client_id, access_token)
        return {"status": "connected", "client_id": client_id} # Dummy return for testing
    except Exception as e:
        st.error(f"Dhan Connection Error: {e}")
        return None

def get_live_ltp(dhan_conn, security_id):
    """Fetches live price using the connection"""
    if dhan_conn:
        try:
            # actual code: 
            # resp = dhan_conn.get_market_quote(exchange_segment='MCX', instrument_token=security_id)
            # return resp['data']['LTP']
            return 72450.0  # Placeholder live price
        except:
            return 0.0
    return 0.0
