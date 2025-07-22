# src/utils/websocket_connector.py

"""
websocket_connector.py

Provides a WebSocket client to subscribe to market streams and dispatch messages.
Requires:
  - websocket-client library
"""

import json
import threading
import websocket  # websocket-client package
from typing import Callable, Any, Optional


class WebsocketConnector:
    """
    Connects to a WebSocket endpoint and relays JSON messages to a handler.
    """

    def __init__(self, url: str, on_message: Callable[[dict], None]):
        """
        Parameters:
            url        (str): WebSocket endpoint URL.
            on_message (callable): Function called with each parsed JSON message.
        """
        self.url = url
        self.on_message = on_message
        self.ws_app: Optional[websocket.WebSocketApp] = websocket.WebSocketApp(
            url,
            on_message=self._handle_message,
            on_error=self._handle_error,
            on_close=self._handle_close
        )
        self._thread: Optional[threading.Thread] = None

    def _handle_message(self, _ws: websocket.WebSocketApp, message: str) -> None:
        try:
            payload = json.loads(message)
        except json.JSONDecodeError:
            return
        self.on_message(payload)

    def _handle_error(self, _ws: websocket.WebSocketApp, error: Exception) -> None:
        # Placeholder for error handling/logging
        # Could log: logger.error(f"WebSocket error: {error}")
        pass

    def _handle_close(
        self,
        _ws: websocket.WebSocketApp,
        close_status_code: int,
        close_msg: str
    ) -> None:
        # Placeholder for close handling/logging
        # Could log: logger.info(f"WebSocket closed: {close_status_code} {close_msg}")
        pass

    def start(self) -> None:
        """
        Launch the WebSocket connection in a background daemon thread.
        """
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(
            target=self.ws_app.run_forever, daemon=True
        )
        self._thread.start()

    def send(self, message: Any) -> None:
        """
        Send a JSON-serializable message to the WebSocket.
        """
        if not self.ws_app:
            return
        try:
            text = json.dumps(message)
            self.ws_app.send(text)
        except (TypeError, json.JSONDecodeError, websocket.WebSocketException):
            # Only catch serialization and WebSocket-specific exceptions
            pass

    def stop(self) -> None:
        """
        Gracefully close the WebSocket and join the thread.
        """
        if self.ws_app:
            self.ws_app.close()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)
