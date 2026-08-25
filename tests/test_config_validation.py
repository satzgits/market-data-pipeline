import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pipeline.config_validation import (
    validate_indicator_config,
    validate_alert_thresholds,
    is_valid
)

GOOD_INDICATORS = {
    "rsi_period": 14,
    "macd_fast": 12,
    "macd_slow": 26,
    "macd_signal": 9,
    "bb_period": 20,
    "bb_std": 2.0,
    "sma_periods": [20, 50, 200],
    "ema_periods": [12, 26],
}

GOOD_ALERTS = {"rsi_oversold": 30, "rsi_overbought": 70}


def test_valid_config_passes():
    assert is_valid(GOOD_INDICATORS, GOOD_ALERTS), "Good config should be valid"


def test_missing_indicator_config():
    cfg = {k: v for k, v in GOOD_INDICATORS.items() if k != "rsi_period"}
    errs = validate_indicator_config(cfg)
    assert any("rsi_period" in e for e in errs)


def test_bad_macd_periods():
    cfg = dict(GOOD_INDICATORS)
    cfg["macd_fast"] = 26
    cfg["macd_slow"] = 12
    assert any("fast" in e for e in validate_indicator_config(cfg))


def test_negative_bollinger_std():
    cfg = dict(GOOD_INDICATORS)
    cfg["bb_std"] = -1.0
    assert any("std-dev" in e for e in validate_indicator_config(cfg))


def test_non_positive_rsi_period():
    cfg = dict(GOOD_INDICATORS)
    cfg["rsi_period"] = 0
    assert any("rsi_period" in e for e in validate_indicator_config(cfg))


def test_inverted_alert_thresholds():
    cfg = {"rsi_oversold": 70, "rsi_overbought": 30}
    assert any("less" in e for e in validate_alert_thresholds(cfg))


def test_alert_thresholds_out_of_range():
    cfg = {"rsi_oversold": 101, "rsi_overbought": -5}
    assert validate_alert_thresholds(cfg), "Out-of-range thresholds should be flagged"


if __name__ == "__main__":
    test_valid_config_passes()
    print("  ✓ Valid config passes")
    test_missing_indicator_config()
    print("  ✓ Missing config flagged")
    test_bad_macd_periods()
    print("  ✓ Bad MACD periods flagged")
    test_negative_bollinger_std()
    print("  ✓ Negative BB std-dev flagged")
    test_non_positive_rsi_period()
    print("  ✓ Non-positive RSI period flagged")
    test_inverted_alert_thresholds()
    print("  ✓ Inverted alert thresholds flagged")
    test_alert_thresholds_out_of_range()
    print("  ✓ Out-of-range thresholds flagged")
    print("\nAll config validation tests passed!")
