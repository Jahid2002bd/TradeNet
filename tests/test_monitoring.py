import json
from src.utils.monitoring import SystemMonitor

def test_log_and_alerts(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    # 높은 threshold → no alerts
    result = SystemMonitor.alert_thresholds({"cpu_pct": 200})
    assert result == {}

    # 로그 쓰기
    SystemMonitor.log_metrics({"cpu_pct": 10, "mem_pct": 20, "disk_pct": 30})
    data = json.loads((tmp_path / "health_log.json").read_text())
    assert isinstance(data, list)
    assert "timestamp" in data[0]
