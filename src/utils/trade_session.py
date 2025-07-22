# src/utils/trade_session.py

"""
trade_session.py

Limits number of trades per day and enforces a cooldown after a loss.
"""

from datetime import datetime, timezone, timedelta


class TradeSession:
    """
    Manages daily trade count and loss cooldowns.
    """

    def __init__(
        self,
        max_trades_per_day: int = 5,
        cooldown_seconds: int = 300
    ):
        """
        Parameters:
            max_trades_per_day (int): Max trades allowed per UTC day.
            cooldown_seconds   (int): Seconds to wait after a loss.
        """
        self.max_trades_per_day = max_trades_per_day
        self.cooldown_period = timedelta(seconds=cooldown_seconds)
        self.trades_executed = 0
        self.last_trade_day = datetime.now(timezone.utc).date()
        self.last_loss_time = None  # datetime of last loss

    def _reset_if_new_day(self, now_utc: datetime) -> None:
        """
        Reset daily counters if UTC date has changed.
        """
        today = now_utc.date()
        if today != self.last_trade_day:
            self.trades_executed = 0
            self.last_trade_day = today
            self.last_loss_time = None

    def can_execute(self, now_utc: datetime) -> bool:
        """
        Check if a new trade can be placed now.
        Returns False if daily limit reached or still in cooldown.
        """
        self._reset_if_new_day(now_utc)

        if self.trades_executed >= self.max_trades_per_day:
            return False

        if (
            self.last_loss_time
            and now_utc - self.last_loss_time < self.cooldown_period
        ):
            return False

        return True

    def record_trade(
        self,
        result: str,
        now_utc: datetime
    ) -> None:
        """
        Record a trade outcome. Increments daily count and marks cooldown on loss.
        """
        self._reset_if_new_day(now_utc)
        self.trades_executed += 1

        if result.lower() == "loss":
            self.last_loss_time = now_utc


if __name__ == "__main__":
    # Demo usage
    session = TradeSession(max_trades_per_day=3, cooldown_seconds=60)
    demo_now = datetime.now(timezone.utc)

    for outcome in ["win", "win", "loss", "win", "win"]:
        allowed = session.can_execute(demo_now)
        print(f"Can execute at {demo_now.time()}: {allowed}")
        session.record_trade(outcome, demo_now)
