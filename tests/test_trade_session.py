from datetime import datetime, timezone, timedelta
from src.utils.trade_session import TradeSession

def test_limits_and_cooldown():
    ts = TradeSession(max_trades_per_day=2, cooldown_seconds=5)
    now = datetime.now(timezone.utc)

    assert ts.can_execute(now)
    ts.record_trade("win", now)
    # 즉시 재실행 불가
    assert not ts.can_execute(now)

    later = now + timedelta(seconds=5)
    assert ts.can_execute(later)
    ts.record_trade("loss", later)
    # 일일 한도 초과
    assert not ts.can_execute(later)
