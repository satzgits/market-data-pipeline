import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from pipeline.alerts import AlertEngine


def test_rsi_oversold_alert():
    engine = AlertEngine()
    row = {"rsi": 25, "close": 100, "macd_line": 1.0, "macd_signal": 0.5,
           "bb_upper": 110, "bb_lower": 90, "mfi": 40}
    alerts = engine.evaluate("TEST", row)
    types = [a[0] for a in alerts]
    assert "RSI_OVERSOLD" in types
    assert "BB_LOWER_TOUCH" not in types


def test_mfi_oversold_alert():
    engine = AlertEngine()
    row = {"rsi": 50, "mfi": 20, "close": 100}
    alerts = engine.evaluate("TEST", row)
    assert ("MFI_OVERSOLD",) == tuple(a[0] for a in alerts if a[0].startswith("MFI"))


def test_no_alert_when_all_normal():
    engine = AlertEngine()
    row = {"rsi": 50, "close": 100, "macd_line": 1.0, "macd_signal": 0.5,
           "bb_upper": 110, "bb_lower": 90, "mfi": 50}
    assert engine.evaluate("TEST", row) == []


def test_recent_window():
    engine = AlertEngine()
    for i in range(5):
        engine.evaluate(f"SYM{i}", {"rsi": 10, "close": 100})
    assert len(engine.recent(3)) == 3
    assert engine.recent(3)[-1]["symbol"] == "SYM4"
