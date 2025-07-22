from src.utils.alerts_dispatcher import AlertsDispatcher

def test_dispatch_no_config():
    dispatcher = AlertsDispatcher()
    outcome = dispatcher.dispatch_alerts("subj", "body", slack_message="hi")
    assert outcome["email"] is False
    # slack not configured → key may be absent or False
    assert outcome.get("slack") is False
