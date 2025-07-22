# src/utils/position_sizing.py

"""
position_sizing.py

Calculates recommended lot size based on account balance,
risk percentage, entry price, and stop loss price.
"""

def calculate_lot_size(
    account_balance: float,
    risk_percent: float,
    entry_price: float,
    stop_loss_price: float
) -> float:
    """
    Calculate lot size so that risk does not exceed a fixed percentage of account balance.

    Parameters:
        account_balance   (float): Current account equity.
        risk_percent      (float): Risk percentage per trade (e.g., 1 for 1%).
        entry_price       (float): Price at which the trade is entered.
        stop_loss_price   (float): Price at which the stop loss is placed.

    Returns:
        float: Calculated lot size (rounded to 3 decimal places).
               Returns 0.0 if stop loss distance is zero or invalid.
    """
    # Determine absolute risk amount in currency
    risk_amount = (risk_percent / 100) * account_balance

    # Calculate distance between entry and stop loss
    stop_loss_distance = abs(entry_price - stop_loss_price)
    if stop_loss_distance <= 0:
        # Prevent division by zero or negative distances
        return 0.0

    # Lot size = risk amount divided by price distance
    lot_size = risk_amount / stop_loss_distance
    return round(lot_size, 3)


if __name__ == "__main__":
    # Example demonstration
    balance = 1000.0      # $1,000 account balance
    risk_pct = 1.0        # 1% risk per trade
    entry = 38000.0       # Entry price
    sl = 37800.0          # Stop loss price

    lot = calculate_lot_size(balance, risk_pct, entry, sl)
    print(f"Account Balance: ${balance}")
    print(f"Risk Percent: {risk_pct}%")
    print(f"Entry Price: {entry}, Stop Loss: {sl}")
    print(f"Recommended Lot Size: {lot}")
