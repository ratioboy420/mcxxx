def calculate_spread_math(near_ltp, far_ltp, side):
    """
    Calculates the spread and dynamic Target/Stop-Loss.
    Spread = Near Leg Price - Far Leg Price
    """
    if near_ltp == 0 or far_ltp == 0:
        return 0, 0, 0
        
    current_spread = near_ltp - far_ltp
    
    # Basic algorithmic logic for SL and Target (Isme hum aage Z-score add karenge)
    # Example: Target is 20 points profit, SL is 10 points loss
    if side == "LONG":
        target = current_spread + 20
        stop_loss = current_spread - 10
    else: # SHORT
        target = current_spread - 20
        stop_loss = current_spread + 10
        
    return current_spread, target, stop_loss
