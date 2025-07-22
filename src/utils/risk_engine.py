# src/utils/risk_engine.py

"""
risk_engine.py

Provides Stop Loss / Take Profit calculation and Risk:Reward validation.
Integrates with position_sizing to tie lot size to risk.
"""

import warnings
from src.utils.position_sizing import calculate_lot_size

# Suppress any runtime warnings
warnings.filterwarnings("ignore")


def suggest_take_profit(
    entry_price: float,
    stop_loss_price: float,
    rr_ratio: float = 2.0,
    position_type: str = "long"
) -> float:
    """
    Compute a take-profit level matching the desired Reward-to-Risk ratio.
    """
    risk_distance = abs(entry_price - stop_loss_price)
    if position_type.lower() == "long":
        return round(entry_price + risk_distance * rr_ratio, 2)
    elif position_type.lower() == "short":
        return round(entry_price - risk_distance * rr_ratio, 2)
    return entry_price


def check_risk_reward(
    entry_price: float,
    stop_loss_price: float,
    take_profit_price: float,
    min_rr_ratio: float = 2.0
) -> bool:
    """
    Validate that Take Profit / Stop Loss satisfy the minimum Reward-to-Risk.
    """
    risk_amount = abs(entry_price - stop_loss_price)
    if risk_amount <= 0:
        return False
    reward_amount = abs(take_profit_price - entry_price)
    return (reward_amount / risk_amount) >= min_rr_ratio


def prepare_trade_parameters(
    account_balance: float,
    risk_percent: float,
    entry_price: float,
    stop_loss_price: float,
    rr_ratio: float = 2.0,
    position_type: str = "long"
) -> dict:
    """
    Bundle lot size, SL, TP and RR validation into one call.
    Returns a dict with:
      - lot_size
      - stop_loss
      - take_profit
      - rr_valid
    """
    lot_size = calculate_lot_size(
        account_balance, risk_percent, entry_price, stop_loss_price
    )
    take_profit = suggest_take_profit(
        entry_price, stop_loss_price, rr_ratio, position_type
    )
    rr_valid = check_risk_reward(
        entry_price, stop_loss_price, take_profit, rr_ratio
    )

    return {
        "lot_size": lot_size,
        "stop_loss": stop_loss_price,
        "take_profit": take_profit,
        "rr_valid": rr_valid
    }


if __name__ == "__main__":
    # Demo usage with unique variable names to avoid shadowing warnings
    demo_balance = 1000.0
    demo_risk_percent = 1.0
    demo_entry = 38000.0
    demo_sl = 37800.0
    demo_rr = 2.0

    params = prepare_trade_parameters(
        demo_balance,
        demo_risk_percent,
        demo_entry,
        demo_sl,
        demo_rr,
        position_type="long"
    )

    print("Trade Parameters:")
    for key, value in params.items():
        print(f"  {key}: {value}")
