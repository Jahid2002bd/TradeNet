import json
from datetime import datetime, timezone, timedelta
from src.utils.weekly_review import WeeklyReview

def test_summarize(tmp_path):
    now = datetime.now(timezone.utc)
    path = tmp_path / "weekly.json"
    entries = [
        {
            "timestamp": (now - timedelta(days=i)).isoformat(),
            "result": res,
            "pnl": 10.0 if res == "win" else -5.0
        }
        for i, res in enumerate(["win", "loss", "win"])
    ]
    path.write_text(json.dumps(entries))

    wr = WeeklyReview(log_path=str(path))
    summary = wr.summarize()

    assert summary["total_trades"] == 3
    assert summary["wins"] == 2
    assert summary["losses"] == 1
    assert isinstance(summary["suggestions"], list)
