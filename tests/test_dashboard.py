import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pipeline.dashboard import Dashboard


def make_sample_row():
    return {
        "close": 101.5,
        "rsi": 55.3,
        "macd_line": 0.8,
        "bb_upper": 105.0,
        "bb_lower": 98.5,
    }


def test_update_and_summary():
    d = Dashboard()
    row = make_sample_row()
    d.update_bar("BTCUSDT", row)
    s = d.summary()
    assert s["symbols"] == ["BTCUSDT"]
    assert s["latest_bars"]["BTCUSDT"]["close"] == 101.5
    assert s["latest_bars"]["BTCUSDT"]["rsi"] == 55.3


def test_alerts_trimmed():
    d = Dashboard()
    for i in range(15):
        d.add_alert({"time": f"t{i}", "message": f"msg{i}"})
    s = d.summary()
    assert len(s["recent_alerts"]) == 10, "should keep at most 10 alerts"


def test_alert_shift():
    d = Dashboard()
    for i in range(5):
        d.add_alert({"time": f"t{i}", "message": f"msg{i}"})
    assert d.recent_alerts[-1]["message"] == "msg4"


if __name__ == "__main__":
    test_update_and_summary()
    print("  ✓ update + summary")
    test_alerts_trimmed()
    print("  ✓ alerts trimmed to 10")
    test_alert_shift()
    print("  ✓ newest alert last")
    print("\nAll dashboard tests passed!")
