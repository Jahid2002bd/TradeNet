from src.utils.backtester import backtest_signals, compute_performance_metrics

def test_backtest_and_metrics():
    closes = [100, 102, 101]
    signals = [1, 0, -1]
    result = backtest_signals(closes, signals, initial_capital=1000)

    equity_curve = result.get("equity_curve")
    assert equity_curve is not None
    assert len(equity_curve) == len(closes)

    metrics = compute_performance_metrics(equity_curve)
    assert "total_return_pct" in metrics
    assert "max_drawdown_pct" in metrics
