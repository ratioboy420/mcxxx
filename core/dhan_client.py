import datetime
import streamlit as st
from dhanhq import dhanhq

# 🔴 APNI ASALI DETAILS YAHAN DAALEIN 🔴
MY_CLIENT_ID = "YOUR_CLIENT_ID_HERE"
MY_ACCESS_TOKEN = "YOUR_ACCESS_TOKEN_HERE"

@st.cache_resource(show_spinner=False)
def get_permanent_connection():
    """Auto-connects to Dhan on startup and stays alive forever."""
    try:
        conn = dhanhq(MY_CLIENT_ID, MY_ACCESS_TOKEN)
        return conn
    except Exception as e:
        st.error(f"Auto-Login Error: {e}")
        return None

def get_live_ltp(dhan_conn, security_id):
    """Fetches live price, safely bypassing library errors."""
    if not dhan_conn or not security_id: 
        return 0.0
    try:
        resp = None
        if hasattr(dhan_conn, 'get_market_quote'):
            resp = dhan_conn.get_market_quote(exchange_segment='MCX', instrument_token=str(security_id))
        elif hasattr(dhan_conn, 'market_quote'):
            resp = dhan_conn.market_quote(exchange_segment='MCX', instrument_token=str(security_id))
            
        if isinstance(resp, dict) and 'data' in resp:
            return float(resp['data'].get('LTP', resp['data'].get('last_price', 0.0)))
        return 0.0
    except:
        return 0.0

def get_historical_prices(dhan_conn, security_id, days=25):
    """Fetches historical data for Z-Score/RSI safely."""
    if not dhan_conn or not security_id: 
        return []
    try:
        to_date = datetime.datetime.now().strftime('%Y-%m-%d')
        from_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
        
        resp = None
        if hasattr(dhan_conn, 'historical_minute_charts'):
            resp = dhan_conn.historical_minute_charts(
                symbol=str(security_id), exchange_segment='MCX', instrument_type='FUTCOM', 
                expiry_code=0, from_date=from_date, to_date=to_date
            )
        elif hasattr(dhan_conn, 'get_historical_data'):
            resp = dhan_conn.get_historical_data(
                symbol=str(security_id), exchange_segment='MCX', instrument_type='FUTCOM', 
                expiry_code=0, from_date=from_date, to_date=to_date
            )
            
        if isinstance(resp, dict) and 'data' in resp and 'close' in resp['data']:
            return resp['data']['close']
        return []
    except:
        return []
