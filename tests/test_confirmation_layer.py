from src.utils.confirmation_engine import confirm_trade_message

def test_confirm_trade_message():
    msg = confirm_trade_message(
        symbol="BTCUSDT",
        entry=100,
        stop_loss=95,
        take_profit=105,
        rsi=75,
        macd_line=1.2,
        signal_line=1.0,
        volume=150000,
        avg_volume=90000,
        ai_confidence=85.0
    )
    assert msg is not None
    assert "Confirmed trade BTCUSDT" in msg
    assert "Enter at 100" in msg
    assert "SL at 95" in msg
    assert "TP at 105" in msg
