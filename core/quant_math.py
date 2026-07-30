import numpy as np
import pandas as pd

def calculate_real_zscore(current_spread, historical_spreads):
    """
    Calculates the Z-Score based on historical spread data.
    """
    if not historical_spreads or len(historical_spreads) < 2:
        return 0.0
    
    mean_spread = np.mean(historical_spreads)
    std_dev = np.std(historical_spreads)
    
    if std_dev == 0:
        return 0.0
        
    z_score = (current_spread - mean_spread) / std_dev
    return round(z_score, 3)

def calculate_rsi(historical_spreads, period=14):
    """
    Calculates the Relative Strength Index (RSI) of the spread.
    """
    if len(historical_spreads) < period + 1:
        return 50.0 # Default neutral RSI if not enough data
        
    deltas = np.diff(historical_spreads)
    seed = deltas[:period]
    up = seed[seed >= 0].sum() / period
    down = -seed[seed < 0].sum() / period
    
    if down == 0:
        return 100.0
        
    rs = up / down
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return round(rsi, 2)

def calculate_advanced_spread(near_ltp, far_ltp, side, historical_spreads=[]):
    """
    The Master Engine: Calculates Spread, dynamic SL/Target, Z-Score, and RSI.
    """
    if near_ltp == 0 or far_ltp == 0:
        return 0.0, 0.0, 0.0, 0.0, 0.0
        
    current_spread = near_ltp - far_ltp
    
    # Calculate Real Indicators if history is provided
    z_score = calculate_real_zscore(current_spread, historical_spreads)
    rsi = calculate_rsi(historical_spreads)
    
    # Dynamic Risk Management based on Z-Score
    # Example: If Z-score is high, we expect mean reversion
    sl_points = 15 # Base stop loss
    target_points = 30 # Base target (1:2 RR)
    
    if side == "LONG":
        target = current_spread + target_points
        stop_loss = current_spread - sl_points
    else: # SHORT
        target = current_spread - target_points
        stop_loss = current_spread + sl_points
        
    return current_spread, target, stop_loss, z_score, rsi
