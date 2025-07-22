# src/utils/weekly_review.py

"""
weekly_review.py

Loads a trade log from JSON, computes weekly performance metrics,
and generates strategy adjustment suggestions.
Requires:
  - trade log as JSON list of:
      {
        "timestamp": ISO8601 string,
        "symbol": str,
        "entry": float,
        "exit": float,
        "result": "win" or "loss",
        "pnl": float
      }
"""

import os
import json
from datetime import datetime, timezone, timedelta
from statistics import mean


class WeeklyReview:
    """
    Processes a JSON trade log and summarizes performance over the last 7 days.
    """

    def __init__(self, log_path: str = "trade_log.json"):
        self.log_path = log_path
        self.trades = self._load_log()

    def _load_log(self) -> list[dict]:
        """Load JSON trade log or return empty list if missing/invalid."""
        if not os.path.exists(self.log_path):
            return []
        try:
            with open(self.log_path, "r", encoding="utf-8") as file_in:
                data = json.load(file_in)
        except json.JSONDecodeError:
            # Malformed JSON
            return []
        except (FileNotFoundError, PermissionError):
            # File inaccessible
            return []

        return data if isinstance(data, list) else []

    def _filter_last_week(self) -> list[dict]:
        """Return trades with timestamp within the past 7 days."""
        cutoff = datetime.now(timezone.utc) - timedelta(days=7)
        recent = []
        for entry in self.trades:
            ts_str = entry.get("timestamp")
            if not ts_str:
                continue
            try:
                ts = datetime.fromisoformat(ts_str).astimezone(timezone.utc)
            except ValueError:
                # Invalid timestamp format
                continue
            if ts >= cutoff:
                recent.append(entry)
        return recent

    def summarize(self) -> dict:
        """
        Compute:
          - total_trades, wins, losses, win_rate
          - total_pnl, avg_pnl
        and generate simple suggestions.
        """
        recent = self._filter_last_week()
        total = len(recent)
        wins = sum(1 for t in recent if t.get("result") == "win")
        losses = sum(1 for t in recent if t.get("result") == "loss")
        win_rate = round((wins / total * 100), 2) if total > 0 else 0.0

        pnl_list = [t.get("pnl", 0.0) for t in recent]
        total_pnl = round(sum(pnl_list), 2)
        avg_pnl = round(mean(pnl_list), 2) if pnl_list else 0.0

        suggestions = []
        if win_rate < 50.0:
            suggestions.append("Review entry criteria—win rate below 50%.")
        if avg_pnl < 0:
            suggestions.append("Strategy in drawdown—consider reducing position size.")
        if total < 5:
            suggestions.append("Low trade volume—evaluate signal frequency or expand watchlist.")
        if not suggestions:
            suggestions.append("Performance looks stable—continue current strategy.")

        return {
            "total_trades": total,
            "wins": wins,
            "losses": losses,
            "win_rate_pct": win_rate,
            "total_pnl": total_pnl,
            "avg_pnl": avg_pnl,
            "suggestions": suggestions
        }


if __name__ == "__main__":
    # Demo: create sample log if missing
    demo_path = "trade_log.json"
    sample_log = [
        {
            "timestamp": (datetime.now(timezone.utc) - timedelta(days=i)).isoformat(),
            "symbol": "BTCUSDT",
            "entry": 38000 + i * 100,
            "exit": 38100 + i * 100,
            "result": "win" if i % 2 == 0 else "loss",
            "pnl": 100.0 if i % 2 == 0 else -50.0
        }
        for i in range(8)
    ]

    if not os.path.exists(demo_path):
        try:
            with open(demo_path, "w", encoding="utf-8") as file_out:
                json.dump(sample_log, file_out, indent=2)
        except PermissionError:
            print(f"Cannot write to {demo_path}, permission denied.")

    review = WeeklyReview(log_path=demo_path)
    report = review.summarize()
    print("Weekly Performance Summary:")
    for key, value in report.items():
        print(f"  {key}: {value}")
