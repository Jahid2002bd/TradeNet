"""
ui_renderer.py

Converts OHLC data list into a Chart.js–compatible chart structure.
"""

from typing import List, Dict, Any

def render_chart(ohlc: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Converts OHLC data to chart-friendly dict.
    Parameters:
        ohlc (List[Dict]): Each entry has open_time, open, high, low, close, volume.
    Returns:
        Dict: {
            "labels": [...],
            "datasets": [
                {"label": "Close Price", "data": [...]}
            ]
        }
    """
    labels = [item["open_time"] for item in ohlc]
    closes = [item["close"] for item in ohlc]
    dataset = {"label": "Close Price", "data": closes}
    return {"labels": labels, "datasets": [dataset]}
