import csv
from src.utils.report_generator import ReportGenerator

def test_report_files_created(sample_trade_log, tmp_path):
    report_dir = tmp_path / "reports"
    rg = ReportGenerator(log_path=sample_trade_log, report_dir=str(report_dir))
    summary = rg.generate_daily_report()

    json_file = report_dir / f"daily_report_{summary['date']}.json"
    csv_file = report_dir / f"daily_report_{summary['date']}.csv"
    assert json_file.exists()
    assert csv_file.exists()

    with open(csv_file, newline="") as f:
        reader = csv.reader(f)
        headers = next(reader)
        assert headers == ["metric", "value"]
