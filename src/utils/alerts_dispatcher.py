# src/utils/alerts_dispatcher.py

"""
alerts_dispatcher.py

Sends alerts via email and Slack.
"""

import os
import requests
import smtplib
from email.message import EmailMessage
from typing import Dict


class AlertsDispatcher:
    """
    Dispatches alerts to configured channels (email, Slack).
    """

    def __init__(self):
        self.slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USERNAME")
        self.smtp_pass = os.getenv("SMTP_PASSWORD")
        self.email_recipient = os.getenv("ALERT_RECIPIENT_EMAIL")

    def send_slack_alert(self, message: str) -> bool:
        """
        Send alert message to Slack webhook.
        Returns True if sent successfully.
        """
        if not self.slack_webhook:
            return False
        payload = {"text": message}
        try:
            resp = requests.post(self.slack_webhook, json=payload, timeout=5)
            resp.raise_for_status()
            return True
        except requests.RequestException:
            return False

    def send_email_alert(self, email_subject: str, email_body: str) -> bool:
        """
        Send alert email using SMTP.
        Returns True if sent successfully.
        """
        if not all([self.smtp_server, self.smtp_user, self.smtp_pass, self.email_recipient]):
            return False
        msg = EmailMessage()
        msg["From"] = self.smtp_user
        msg["To"] = self.email_recipient
        msg["Subject"] = email_subject
        msg.set_content(email_body)

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as smtp_conn:
                smtp_conn.starttls()
                smtp_conn.login(self.smtp_user, self.smtp_pass)
                smtp_conn.send_message(msg)
            return True
        except (smtplib.SMTPException, ConnectionError):
            return False

    def dispatch_alerts(
        self,
        email_subject: str,
        email_body: str,
        slack_message: str = None
    ) -> Dict[str, bool]:
        """
        Send alerts via both Slack and email (if configured).
        Returns dict of outcomes.
        """
        results = {
            "email": self.send_email_alert(email_subject, email_body)
        }
        if slack_message:
            results["slack"] = self.send_slack_alert(slack_message)
        return results


if __name__ == "__main__":
    dispatcher = AlertsDispatcher()
    alert_subject = "TradeNet Alert"
    alert_body = "Test alert: your trade signal triggered."
    slack_text = "TradeNet: Test alert triggered."
    outcome = dispatcher.dispatch_alerts(
        alert_subject, alert_body, slack_message=slack_text
    )
    print("Alert dispatch results:", outcome)
