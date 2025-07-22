from src.utils.websocket_connector import WebsocketConnector

def test_start_stop(monkeypatch):
    class FakeApp:
        def run_forever(self): pass
        def close(self): pass

    monkeypatch.setattr(
        "src.utils.websocket_connector.websocket.WebSocketApp",
        lambda *args, **kwargs: FakeApp()
    )

    connector = WebsocketConnector("wss://example", lambda msg: None)
    connector.start()
    connector.stop()
