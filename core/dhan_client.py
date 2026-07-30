import datetime
import streamlit as st
from dhanhq import dhanhq

@st.cache_resource
def get_dhan_connection(client_id, access_token):
    """Establishes a persistent connection to Dhan API using stable version"""
    try:
        conn = dhanhq(client_id, access_token)
        return conn
    except Exception as e:
        st.error(f"Dhan Connection Error: {e}")
        return None

def get_live_ltp(dhan_conn, security_id):
    """Fetches live price using the connection"""
    if not dhan_conn or not security_id:
        return 0.0
        
    try:
        # Pinging Dhan API for live price
        resp = dhan_conn.get_market_quote(exchange_segment='MCX', instrument_token=security_id)
        
        # Checking if response is valid
        if isinstance(resp, dict) and 'data' in resp:
            try:
                return float(resp['data']['LTP'])
            except KeyError:
                st.sidebar.warning(f"Unexpected API Response format: {resp}")
                return 0.0
        else:
            st.sidebar.error(f"Failed to fetch market quote. API returned: {resp}")
            return 0.0
            
    except Exception as e:
        st.sidebar.error(f"API Exception for Token {security_id}: {str(e)}")
        return 0.0

def get_historical_prices(dhan_conn, security_id, days=25):
    """
    Fetches historical closing prices from Dhan API to calculate statistical indicators.
    """
    if not dhan_conn or not security_id:
        return []
        
    try:
        to_date = datetime.datetime.now().strftime('%Y-%m-%d')
        from_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
        
        # Calling Dhan's historical data endpoint (Daily interval)
        resp = dhan_conn.historical_minute_charts(
            symbol=str(security_id),
            exchange_segment='MCX',
            instrument_type='FUTCOM',
            expiry_code=0, # 0 means current expiry
            from_date=from_date,
            to_date=to_date
        )
        
        # Dhan returns data in a dictionary under 'data' -> 'close'
        if isinstance(resp, dict) and 'data' in resp and 'close' in resp['data']:
            return resp['data']['close']
        else:
            return []
            
    except Exception as e:
        st.sidebar.error(f"Historical Data API Error for token {security_id}: {e}")
        return []
