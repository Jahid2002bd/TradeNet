from src.utils.risk_engine import check_risk_reward, suggest_take_profit

def test_rr_check_and_suggest():
    assert check_risk_reward(100, 90, 110, 2.0)
    # RR = (110–100)/(100–90) = 1.0, below target → False
    assert not check_risk_reward(100, 95, 105, 2.0)

    # suggest TP for RR=2
    tp = suggest_take_profit(100, 90, 2.0)
    assert tp == 110.0
