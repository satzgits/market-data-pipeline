BINANCE_BASE_URL = "https://api.binance.com/api/v3"
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]

INTERVAL = "1m"

ALPHA_VANTAGE_KEY = "demo"

ALERT_THRESHOLDS = {
    "rsi_oversold": 30,
    "rsi_overbought": 70,
    "bb_std": 2.0,
    "macd_signal_period": 9,
}

INDICATOR_CONFIG = {
    "rsi_period": 14,
    "macd_fast": 12,
    "macd_slow": 26,
    "macd_signal": 9,
    "bb_period": 20,
    "bb_std": 2.0,
    "sma_periods": [20, 50, 200],
    "ema_periods": [12, 26],
}

DASHBOARD_REFRESH_SECONDS = 2
LOG_FILE = "pipeline.log"
