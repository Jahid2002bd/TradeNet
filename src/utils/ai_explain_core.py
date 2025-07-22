# src/utils/ai_explain_core.py

"""
ai_explain_core.py

Generates human-readable explanations for trade signals,
including entry rationale, risk overview, and reward projections.
"""

from src.utils.risk_engine import check_risk_reward, suggest_take_profit
from src.utils.sentiment_analysis import get_sentiment_score


def generate_explanation(
    symbol: str,
    entry_price: float,
    stop_loss_price: float,
    take_profit_price: float,
    rr_ratio: float = None
) -> str:
    """
    Build a detailed explanation string for the proposed trade.
    """
    # Compute distances
    risk_distance = abs(entry_price - stop_loss_price)
    reward_distance = abs(take_profit_price - entry_price)
    actual_rr = round(reward_distance / risk_distance, 2) if risk_distance > 0 else None

    # Check RR target if provided
    meets_rr = True
    rr_suggestion = ""
    if rr_ratio:
        meets_rr = check_risk_reward(
            entry_price, stop_loss_price, take_profit_price, rr_ratio
        )
        suggested_tp = suggest_take_profit(
            entry_price, stop_loss_price, rr_ratio
        )
        rr_suggestion = f" Suggested TP for {rr_ratio}:1 RR is {suggested_tp}."

    # Fetch sentiment context
    sentiment = get_sentiment_score(symbol)
    sentiment_str = f"News sentiment score for {symbol} is {sentiment:.2f}."

    explanation_lines = [
        f"Signal for {symbol}:",
        f"Entry at {entry_price}, SL at {stop_loss_price} (risk {risk_distance}).",
        f"TP at {take_profit_price} (reward {reward_distance}, RR = {actual_rr}).",
        ("RR meets target." if meets_rr else "RR below target."),
        sentiment_str + rr_suggestion
    ]

    return " ".join(explanation_lines)
