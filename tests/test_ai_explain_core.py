from src.utils.ai_explain_core import generate_explanation

def test_generate_explanation_structure(dummy_market):
    text = generate_explanation(
        symbol="BTCUSDT",
        entry_price=1000,
        stop_loss_price=990,
        take_profit_price=1010,
        rr_ratio=1.5
    )
    assert "Entry at 1000" in text
    assert "News sentiment" in text
    assert "RR meets target" in text or "RR below target" in text
