# src/utils/monitoring.py

"""
monitoring.py

Tracks system health metrics and alerts on thresholds.
Requires psutil and src.utils.alerts_dispatcher.AlertsDispatcher.
"""

import json
import logging
from datetime import datetime, timezone
import os

import psutil
from src.utils.alerts_dispatcher import AlertsDispatcher

HEALTH_LOG = "health_log.json"
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class SystemMonitor:
    """
    Gathers system metrics, writes health logs, and alerts if thresholds exceeded.
    """

    @staticmethod
    def get_metrics() -> dict:
        """
        Return CPU, memory, and disk usage percentages.
        """
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        return {"cpu_pct": cpu, "mem_pct": mem, "disk_pct": disk}

    @staticmethod
    def log_metrics(metrics: dict) -> None:
        """
        Append a timestamped metrics entry to the health log.
        """
        entry = {"timestamp": datetime.now(timezone.utc).isoformat(), **metrics}
        try:
            if os.path.exists(HEALTH_LOG):
                with open(HEALTH_LOG, "r", encoding="utf-8") as inp:
                    data = json.load(inp)
                if not isinstance(data, list):
                    data = []
            else:
                data = []
        except (json.JSONDecodeError, IOError):
            data = []

        data.append(entry)
        try:
            with open(HEALTH_LOG, "w", encoding="utf-8") as outp:
                json.dump(data, outp, indent=2)
        except IOError:
            logger.warning("Failed to write health log.")

    @staticmethod
    def alert_thresholds(
        thresholds: dict
    ) -> dict:
        """
        Check metrics against thresholds and send alerts.
        Returns dict of channel results.
        """
        metrics = SystemMonitor.get_metrics()
        alerts = {}
        dispatcher = AlertsDispatcher()

        for key, limit in thresholds.items():
            val = metrics.get(key)
            if val is not None and val >= limit:
                msg = f"Alert: {key} at {val:.1f}% (threshold {limit}%)"
                alerts[key] = dispatcher.send_slack_alert(msg)
                logger.info(msg)

        return alerts
