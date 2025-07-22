from src.utils.chatbot_ui import handle_user_query

def test_handle_user_query_valid():
    resp = handle_user_query("explain BTCUSDT 100 95 105 2")
    assert "Signal for BTCUSDT" in resp

def test_handle_user_query_invalid():
    resp = handle_user_query("bad command")
    assert "Use command" in resp
