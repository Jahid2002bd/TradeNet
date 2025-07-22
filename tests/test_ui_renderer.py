from src.utils.ui_renderer import render_chart

def test_render_chart_minimal():
    ohlc = [{
        "open_time": "2025-07-21T00:00:00Z",
        "open": 1.0,
        "high": 2.0,
        "low": 0.5,
        "close": 1.5,
        "volume": 100.0
    }]
    chart = render_chart(ohlc)
    assert chart["labels"] == ["2025-07-21T00:00:00Z"]
    assert chart["datasets"][0]["label"] == "Close Price"
    assert chart["datasets"][0]["data"] == [1.5]
