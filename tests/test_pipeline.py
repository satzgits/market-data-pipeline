import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np
from pipeline.indicators import TechnicalIndicators


def make_sample_data(length=100):
    np.random.seed(42)
    prices = 100 + np.cumsum(np.random.randn(length) * 0.5)
    dates = pd.date_range("2024-01-01", periods=length, freq="h")
    return pd.DataFrame({
        "open": prices * 0.99,
        "high": prices * 1.02,
        "low": prices * 0.98,
        "close": prices,
        "volume": np.random.randint(1000, 5000, size=length)
    }, index=dates)


def test_rsi():
    df = make_sample_data(200)
    ti = TechnicalIndicators()
    result = ti.rsi(df)
    assert "rsi" in result.columns
    rsi_vals = result["rsi"].dropna()
    assert (rsi_vals >= 0).all() and (rsi_vals <= 100).all()
    print("  ✓ RSI computed correctly")


def test_macd():
    df = make_sample_data(200)
    ti = TechnicalIndicators()
    result = ti.macd(df)
    assert "macd_line" in result.columns
    assert "macd_signal" in result.columns
    assert "macd_histogram" in result.columns
    print("  ✓ MACD computed correctly")


def test_bollinger_bands():
    df = make_sample_data(200)
    ti = TechnicalIndicators()
    result = ti.bollinger_bands(df)
    assert "bb_upper" in result.columns
    assert "bb_lower" in result.columns
    assert "bb_middle" in result.columns
    assert (result["bb_upper"] >= result["bb_middle"]).all()
    assert (result["bb_middle"] >= result["bb_lower"]).all()
    print("  ✓ Bollinger Bands computed correctly")


def test_compute_all():
    df = make_sample_data(200)
    ti = TechnicalIndicators({
        "rsi_period": 14,
        "macd_fast": 12, "macd_slow": 26, "macd_signal": 9,
        "bb_period": 20, "bb_std": 2.0,
        "sma_periods": [20, 50],
        "ema_periods": [12, 26],
    })
    result = ti.compute_all(df)
    expected_cols = ["rsi", "macd_line", "macd_signal", "bb_upper", "bb_lower", "sma_20", "sma_50", "ema_12", "ema_26"]
    for col in expected_cols:
        assert col in result.columns, f"Missing column: {col}"
    print("  ✓ All indicators computed")


if __name__ == "__main__":
    test_rsi()
    test_macd()
    test_bollinger_bands()
    test_compute_all()
    print("\nAll pipeline tests passed!")
