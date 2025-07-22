# src/utils/notifications.py

"""
notifications.py

Sends notifications via Telegram and Firebase Cloud Messaging (FCM),
and records in‐app notifications locally.
Requires:
  - TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID environment variables
  - FCM_SERVER_KEY and optional FCM_DEVICE_TOKENS (comma-separated) env vars
"""

import os
import json
import requests
from typing import Dict

NOTIFICATION_LOG = os.getenv("NOTIFICATION_LOG_PATH", "notifications.json")


class NotificationService:
    """
    Service to dispatch notifications via Telegram, FCM, and local log.
    """

    @staticmethod
    def send_telegram(message: str) -> bool:
        """
        Send a message via Telegram bot.
        """
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if not token or not chat_id:
            return False

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
        try:
            resp = requests.post(url, json=payload, timeout=5)
            resp.raise_for_status()
            return True
        except requests.RequestException:
            return False

    @staticmethod
    def send_fcm(title: str, body: str) -> bool:
        """
        Send a push notification via Firebase Cloud Messaging.
        """
        server_key = os.getenv("FCM_SERVER_KEY")
        tokens = os.getenv("FCM_DEVICE_TOKENS", "")
        device_tokens = [t.strip() for t in tokens.split(",") if t.strip()]
        if not server_key or not device_tokens:
            return False

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"key={server_key}"
        }
        payload = {
            "registration_ids": device_tokens,
            "notification": {"title": title, "body": body}
        }
        try:
            resp = requests.post(
                "https://fcm.googleapis.com/fcm/send",
                headers=headers,
                json=payload,
                timeout=5
            )
            resp.raise_for_status()
            return True
        except requests.RequestException:
            return False

    @staticmethod
    def record_local(notification: Dict[str, str]) -> None:
        """
        Append a notification record to local JSON store.
        """
        try:
            if os.path.exists(NOTIFICATION_LOG):
                with open(NOTIFICATION_LOG, "r", encoding="utf-8") as inp:
                    data = json.load(inp)
                if not isinstance(data, list):
                    data = []
            else:
                data = []
        except (json.JSONDecodeError, IOError):
            data = []

        data.append(notification)
        try:
            with open(NOTIFICATION_LOG, "w", encoding="utf-8") as outp:
                json.dump(data, outp, indent=2)
        except IOError:
            pass
