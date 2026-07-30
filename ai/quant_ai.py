import time

def get_ai_trade_decision(metal, near_exp, far_exp):
    """
    Connects to Groq and runs your custom Z-Score, RSI, and OI Delta logic.
    Returns the Side (LONG/SHORT) and the reasoning.
    """
    # TODO: Connect to actual Groq API here in the future
    time.sleep(1.5) # Simulating API latency
    
    # Simulated AI logic based on your technical rules
    recommended_side = "SHORT"
    reason = f"Z-Score is +1.4. Near OI Delta is +14%. AI recommends SHORTING {metal} {near_exp}/{far_exp}."
    
    return recommended_side, reason
