import datetime
import streamlit as st
from dhanhq import dhanhq

# ... (Aapka purana get_dhan_connection aur get_live_ltp code yahan waise hi rahega) ...

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
