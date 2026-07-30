import datetime
import streamlit as st
from dhanhq import dhanhq

@st.cache_resource
def get_dhan_connection(client_id, access_token):
    try:
        return dhanhq(client_id, access_token)
    except Exception as e:
        st.error(f"Dhan Connection Error: {e}")
        return None

def get_live_ltp(dhan_conn, security_id):
    if not dhan_conn or not security_id:
        return 0.0
        
    try:
        resp = None
        # Smart Hunt: Searching for the exact method name existing in this version
        if hasattr(dhan_conn, 'get_market_quote'):
            resp = dhan_conn.get_market_quote(exchange_segment='MCX', instrument_token=str(security_id))
        elif hasattr(dhan_conn, 'market_quote'):
            resp = dhan_conn.market_quote(exchange_segment='MCX', instrument_token=str(security_id))
        else:
            # Agar koi function nahi mila, print the available methods so we can see what to use
            methods = [m for m in dir(dhan_conn) if not m.startswith('_')]
            st.sidebar.error(f"No valid price method found. Available methods: {methods}")
            return 0.0

        if isinstance(resp, dict) and 'data' in resp:
            try:
                return float(resp['data']['LTP'])
            except KeyError:
                try:
                    return float(resp['data'].get('last_price', 0.0))
                except:
                    return 0.0
        return 0.0
        
    except Exception as e:
        st.sidebar.error(f"LTP Error for {security_id}: {str(e)}")
        return 0.0

def get_historical_prices(dhan_conn, security_id, days=25):
    if not dhan_conn or not security_id:
        return []
        
    try:
        to_date = datetime.datetime.now().strftime('%Y-%m-%d')
        from_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
        
        resp = None
        # Smart Hunt for Historical method
        if hasattr(dhan_conn, 'historical_minute_charts'):
            resp = dhan_conn.historical_minute_charts(
                symbol=str(security_id),
                exchange_segment='MCX',
                instrument_type='FUTCOM',
                expiry_code=0,
                from_date=from_date,
                to_date=to_date
            )
        elif hasattr(dhan_conn, 'get_historical_data'):
             resp = dhan_conn.get_historical_data(
                symbol=str(security_id), exchange_segment='MCX', instrument_type='FUTCOM',
                expiry_code=0, from_date=from_date, to_date=to_date
            )
             
        if isinstance(resp, dict) and 'data' in resp and 'close' in resp['data']:
            return resp['data']['close']
        else:
            return []
            
    except Exception as e:
        st.sidebar.error(f"Hist Error for {security_id}: {e}")
        return []
