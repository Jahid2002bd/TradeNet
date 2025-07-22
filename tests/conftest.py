# tests/conftest.py

import sys
from pathlib import Path
import json
import pytest
from datetime import datetime, timedelta, timezone
from src.utils import market_api_connector

# Ensure 'src/' is discoverable by Python
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

@pytest.fixture(autouse=True)
def isolated_env(tmp_path, monkeypatch):
    """Each test runs inside a temp folder, with clean ENV setup."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("SLACK_WEBHOOK_URL", "")
    monkeypatch.setenv("SMTP_SERVER", "")
    monkeypatch.setenv("FCM_SERVER_KEY", "")
    monkeypatch.setenv("FCM_DEVICE_TOKENS", "")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "")
    yield

@pytest.fixture
def sample_trade_log(tmp_path):
    """Create sample trade_log.json for WeeklyReview or reporting tests."""
    now = datetime.now(timezone.utc)
    entries = []
    for i, result in enumerate(["win", "loss", "win"]):
        entries.append({
            "timestamp": (now - timedelta(days=i)).isoformat(),
            "symbol": "BTCUSDT",
            "entry": 100 + i,
            "exit": 100 + i + (10 if result == "win" else -5),
            "result": result,
            "pnl": 10.0 if result == "win" else -5.0
        })
    path = tmp_path / "trade_log.json"
    path.write_text(json.dumps(entries, indent=2))
    return str(path)

@pytest.fixture
def dummy_market(monkeypatch):
    """Stub market price fetching so it returns 1234.5 for any symbol."""
    monkeypatch.setattr(market_api_connector, "get_binance_price", lambda symbol: 1234.5)
    monkeypatch.setattr(market_api_connector, "get_coinbase_price", lambda symbol: 1234.5)
