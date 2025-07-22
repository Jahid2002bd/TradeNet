# src/utils/backtester.py

"""
backtester.py

Runs a simple signal‐based backtest on OHLC data.
Computes equity curve, total return, win rate, and max drawdown.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Sequence


def backtest_signals(
    close_prices: Sequence[float],
    signals: Sequence[int],
    initial_capital: float = 1000.0,
    lot_size: float = 1.0
) -> Dict[str, np.ndarray]:
    """
    Execute a backtest:
      - enter long when signal == 1, short when -1, flat when 0.
      - PnL at t = (close[t+1] - close[t]) * position[t] * lot_size.
      - Equity curve = initial_capital + cumulative PnL.

    Returns dict with:
      "equity_curve" (np.ndarray),
      "returns" (np.ndarray of per‐step PnL),
      "positions" (np.ndarray).
    """
    closes = np.array(close_prices, dtype=float)
    sigs = np.array(signals, dtype=int)
    n = len(closes)
    if len(sigs) != n:
        raise ValueError("close_prices and signals must be same length.")

    # position held during interval [t, t+1)
    positions = sigs.copy()
    # compute step returns (last point has no next price)
    step_returns = np.zeros(n, dtype=float)
    for idx in range(n - 1):
        step_returns[idx] = (closes[idx + 1] - closes[idx]) * positions[idx] * lot_size

    equity = initial_capital + np.cumsum(step_returns)
    return {
        "equity_curve": equity,
        "returns": step_returns,
        "positions": positions
    }


def compute_performance_metrics(
    equity_curve: np.ndarray
) -> Dict[str, float]:
    """
    Compute:
      - total_return_pct
      - max_drawdown_pct
    """
    peak = np.maximum.accumulate(equity_curve)
    drawdowns = (equity_curve - peak) / peak
    max_dd = float(np.min(drawdowns)) * 100  # negative value
    total_ret = (equity_curve[-1] / equity_curve[0] - 1) * 100
    return {
        "total_return_pct": total_ret,
        "max_drawdown_pct": max_dd
    }


def plot_equity_curve(
    equity_curve: Sequence[float],
    title: str = "Equity Curve"
) -> None:
    """
    Plot equity over time.
    """
    plt.figure(figsize=(8, 4))
    plt.plot(equity_curve, linewidth=2)
    plt.title(title)
    plt.xlabel("Step")
    plt.ylabel("Equity")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # Demo backtest: synthetic close prices and random signals
    import numpy as np

    np.random.seed(42)
    demo_closes = np.cumsum(np.random.normal(0, 1, 100)) + 100
    demo_signals = np.random.choice([1, 0, -1], size=100, p=[0.3, 0.4, 0.3])

    results = backtest_signals(demo_closes, demo_signals)
    metrics = compute_performance_metrics(results["equity_curve"])

    print("Performance Metrics:", metrics)
    plot_equity_curve(results["equity_curve"], title="Demo Equity Curve")
