# src/utils/report_generator.py

"""
report_generator.py

Generates daily and monthly trade performance reports,
saving them as CSV and JSON files in a reports directory.
"""

import os
import json
import csv
from datetime import datetime, timezone, date
from statistics import mean
from typing import List, Dict


class ReportGenerator:
    """
    Processes trade logs to generate performance reports.
    """

    def __init__(self, log_path: str = "trade_log.json", report_dir: str = "reports"):
        self.log_path = log_path
        self.report_dir = report_dir
        self.trades = self._load_log()
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)

    def _load_log(self) -> List[Dict]:
        """
        Load JSON trade log or return empty list.
        """
        if not os.path.exists(self.log_path):
            return []
        try:
            with open(self.log_path, "r", encoding="utf-8") as file_in:
                data_loaded = json.load(file_in)
        except (json.JSONDecodeError, FileNotFoundError, PermissionError):
            return []
        return data_loaded if isinstance(data_loaded, list) else []

    def _filter_trades_by_date(self, target_date: date) -> List[Dict]:
        """
        Return trades executed on target_date (UTC).
        """
        selected: List[Dict] = []
        for trade_entry in self.trades:
            ts_str = trade_entry.get("timestamp")
            if not isinstance(ts_str, str):
                continue
            try:
                trade_dt = datetime.fromisoformat(ts_str).astimezone(timezone.utc)
            except ValueError:
                continue
            if trade_dt.date() == target_date:
                selected.append(trade_entry)
        return selected

    def generate_daily_report(self, target_date: date = None) -> Dict:
        """
        Generate report for target_date (UTC). Defaults to today UTC.
        Saves daily_report_<YYYY-MM-DD>.[csv|json] in report_dir.
        Returns summary dict.
        """
        report_date = target_date or datetime.now(timezone.utc).date()
        trades_today = self._filter_trades_by_date(report_date)

        total_trades = len(trades_today)
        wins_count = sum(1 for t in trades_today if t.get("result") == "win")
        losses_count = sum(1 for t in trades_today if t.get("result") == "loss")
        win_rate_pct = round((wins_count / total_trades * 100), 2) if total_trades > 0 else 0.0
        pnl_values = [t.get("pnl", 0.0) for t in trades_today]
        total_pnl = round(sum(pnl_values), 2)
        avg_pnl = round(mean(pnl_values), 2) if pnl_values else 0.0

        summary = {
            "date": report_date.isoformat(),
            "total_trades": total_trades,
            "wins": wins_count,
            "losses": losses_count,
            "win_rate_pct": win_rate_pct,
            "total_pnl": total_pnl,
            "avg_pnl": avg_pnl
        }

        # Write JSON
        json_path = os.path.join(
            self.report_dir, f"daily_report_{report_date.isoformat()}.json"
        )
        try:
            with open(json_path, "w", encoding="utf-8") as file_out:
                json.dump(summary, file_out, indent=2)
        except PermissionError:
            pass

        # Write CSV
        csv_path = os.path.join(
            self.report_dir, f"daily_report_{report_date.isoformat()}.csv"
        )
        try:
            with open(csv_path, "w", newline="", encoding="utf-8") as file_out:
                writer = csv.writer(file_out)
                writer.writerow(["metric", "value"])
                for key, val in summary.items():
                    writer.writerow([key, val])
        except PermissionError:
            pass

        return summary

    def generate_monthly_report(self, year: int = None, month: int = None) -> Dict:
        """
        Generate monthly report for given year and month (UTC).
        Defaults to current month. Saves monthly_report_<YYYYMM>.[csv|json].
        """
        now_utc = datetime.now(timezone.utc)
        report_year = year or now_utc.year
        report_month = month or now_utc.month

        trades_filtered: List[Dict] = []
        for trade_entry in self.trades:
            ts_str = trade_entry.get("timestamp")
            if not isinstance(ts_str, str):
                continue
            try:
                trade_dt = datetime.fromisoformat(ts_str).astimezone(timezone.utc)
            except ValueError:
                continue
            if trade_dt.year == report_year and trade_dt.month == report_month:
                trades_filtered.append(trade_entry)

        total_trades = len(trades_filtered)
        wins_count = sum(1 for t in trades_filtered if t.get("result") == "win")
        losses_count = sum(1 for t in trades_filtered if t.get("result") == "loss")
        win_rate_pct = round((wins_count / total_trades * 100), 2) if total_trades > 0 else 0.0
        pnl_values = [t.get("pnl", 0.0) for t in trades_filtered]
        total_pnl = round(sum(pnl_values), 2)
        avg_pnl = round(mean(pnl_values), 2) if pnl_values else 0.0

        summary = {
            "year": report_year,
            "month": report_month,
            "total_trades": total_trades,
            "wins": wins_count,
            "losses": losses_count,
            "win_rate_pct": win_rate_pct,
            "total_pnl": total_pnl,
            "avg_pnl": avg_pnl
        }

        json_path = os.path.join(
            self.report_dir, f"monthly_report_{report_year}{report_month:02d}.json"
        )
        try:
            with open(json_path, "w", encoding="utf-8") as file_out:
                json.dump(summary, file_out, indent=2)
        except PermissionError:
            pass

        csv_path = os.path.join(
            self.report_dir, f"monthly_report_{report_year}{report_month:02d}.csv"
        )
        try:
            with open(csv_path, "w", newline="", encoding="utf-8") as file_out:
                writer = csv.writer(file_out)
                writer.writerow(["metric", "value"])
                for key, val in summary.items():
                    writer.writerow([key, val])
        except PermissionError:
            pass

        return summary


if __name__ == "__main__":
    reporter = ReportGenerator(log_path="trade_log.json", report_dir="reports")
    daily_summary = reporter.generate_daily_report()
    print("Daily Report Summary:", daily_summary)
    monthly_summary = reporter.generate_monthly_report()
    print("Monthly Report Summary:", monthly_summary)
