import streamlit as st
import inspect
from dhanhq import dhanhq

@st.cache_resource
def get_dhan_connection(client_id, access_token):
    """Establishes a persistent connection to Dhan API by dynamically reading its requirements"""
    try:
        # Dhan library scan karo ki use kitne aur konse parameters chahiye
        sig = inspect.signature(dhanhq.__init__)
        params = list(sig.parameters.keys())
        
        # Agar library sirf 1 argument (besides 'self') expect kar rahi hai
        if len(params) == 2:  
            try:
                # Jyadatar cases me naya SDK sirf access_token leta hai
                return dhanhq(access_token)
            except Exception:
                # Agar wo dictionary expect kar raha hai
                return dhanhq({"client_id": client_id, "access_token": access_token})
                
        # Agar library 2 arguments expect kar rahi hai, toh uske naam ke hisab se dynamically pass karo
        kwargs = {}
        for param in params:
            if 'client' in param.lower():
                kwargs[param] = client_id
            elif 'token' in param.lower():
                kwargs[param] = access_token
                
        # Connect with dynamic keywords
        if kwargs:
            return dhanhq(**kwargs)
            
        # Absolute Fallback
        return dhanhq(client_id, access_token)

    except Exception as e:
        # Agar fail hua, toh screen par exact parameter names print honge jo Dhan mang raha hai
        st.error(f"Dhan Connection Error. Expected parameters: {params} | Error: {e}")
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
