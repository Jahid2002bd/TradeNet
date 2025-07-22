import requests
from src.utils.notifications import NotificationService

def test_send_telegram_and_fcm(monkeypatch):
    class FakeResponse:
        def raise_for_status(self): pass

    monkeypatch.setattr(requests, "post", lambda *a, **k: FakeResponse())
    assert NotificationService.send_telegram("hello")
    assert NotificationService.send_fcm("title", "body")
