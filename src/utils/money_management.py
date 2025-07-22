"""
money_management.py

Calculates position size based on account balance and risk per trade.
"""

def calculate_position_size(
    account_balance: float,
    risk_per_trade: float,
    entry_price: float,
    stop_loss_price: float
) -> float:
    """
    Compute lot size so that a loss at stop-loss equals risk_per_trade × account_balance.
    Returns:
        float: Position size.
    """
    risk_amount = account_balance * risk_per_trade
    price_diff = abs(entry_price - stop_loss_price)
    if price_diff == 0:
        return 0.0
    raw_size = risk_amount / price_diff
    return round(raw_size, 8)
