# src/utils/money_control.py

"""
money_control.py

Dynamically adjusts position size based on winning or losing streaks.
Prevents Martingale or revenge trades by capping scaling factors.
"""


def update_win_loss_streak(
    previous_streak: int,
    result: str
) -> int:
    """
    Update the win/loss streak counter.
    - If result == "win": increment positive streak or reset from losses.
    - If result == "loss": decrement negative streak or reset from wins.
    """
    res = result.lower()
    if res == "win":
        return previous_streak + 1 if previous_streak >= 0 else 1
    elif res == "loss":
        return previous_streak - 1 if previous_streak <= 0 else -1
    return previous_streak


def calculate_scaled_lot_size(
    base_lot: float,
    streak: int,
    scale_up_pct: float = 0.1,
    scale_down_pct: float = 0.1,
    min_scale: float = 0.5,
    max_scale: float = 2.0
) -> float:
    """
    Scale the base lot size up or down based on current streak.
    - For positive streak: increase by scale_up_pct per win.
    - For negative streak: decrease by scale_down_pct per loss.
    - Cap overall scale factor between min_scale and max_scale.
    """
    if streak > 0:
        factor = 1 + scale_up_pct * streak
    elif streak < 0:
        factor = 1 + scale_down_pct * streak  # streak is negative
    else:
        factor = 1.0

    # Enforce scaling caps
    factor = max(min_scale, min(max_scale, factor))
    return round(base_lot * factor, 3)


if __name__ == "__main__":
    # Demo: starting from a base lot of 0.2
    demo_base_lot = 0.2
    demo_streak = 0

    # Simulate a sequence of trade results
    demo_results = ["win", "win", "loss", "loss", "loss", "win", "win"]

    print(f"Base lot: {demo_base_lot}")
    for outcome in demo_results:
        demo_streak = update_win_loss_streak(demo_streak, outcome)
        adjusted_lot = calculate_scaled_lot_size(demo_base_lot, demo_streak)
        print(f"Result: {outcome:5s} | Streak: {demo_streak:2d} | Adjusted Lot: {adjusted_lot}")
