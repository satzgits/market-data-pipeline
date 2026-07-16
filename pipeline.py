import time
import argparse
import pandas as pd

from config import SYMBOLS, INTERVAL, ALERT_THRESHOLDS, INDICATOR_CONFIG, DASHBOARD_REFRESH_SECONDS
from pipeline.ingestion import DataIngestion
from pipeline.indicators import TechnicalIndicators
from pipeline.alerts import AlertEngine
from pipeline.dashboard import Dashboard


def run_live(symbols=None, interval=None):
    symbols = symbols or SYMBOLS
    interval = interval or INTERVAL

    ingestion = DataIngestion()
    indicators = TechnicalIndicators(INDICATOR_CONFIG)
    alerts = AlertEngine(ALERT_THRESHOLDS)
    dashboard = Dashboard(DASHBOARD_REFRESH_SECONDS)

    print(f"Starting market data pipeline for {symbols} ({interval})...")

    def process_bar(bar):
        symbol = bar["symbol"]
        df = pd.DataFrame([bar]).set_index("timestamp")
        df_with_indicators = indicators.compute_all(df)
        row = df_with_indicators.iloc[-1]
        dashboard.update_bar(symbol, row)
        new_alerts = alerts.evaluate(symbol, row)
        for a in new_alerts:
            dashboard.add_alert({"time": bar["timestamp"], "message": a[1]})
        dashboard.render()

    ws = ingestion.stream_binance_websocket(symbols, process_bar, interval)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nPipeline stopped.")


def run_historical(symbol, interval="1h", limit=500):
    ingestion = DataIngestion()
    indicators = TechnicalIndicators(INDICATOR_CONFIG)
    alerts = AlertEngine(ALERT_THRESHOLDS)

    print(f"Fetching {limit} bars of {symbol} ({interval})...")
    df = ingestion.fetch_binance_klines(symbol, interval, limit)
    df = indicators.compute_all(df)

    print(f"\n{'='*70}")
    print(f"  HISTORICAL ANALYSIS — {symbol} ({interval})")
    print(f"{'='*70}")
    print(f"  Period: {df.index[0]} to {df.index[-1]}")
    print(f"  Bars:   {len(df)}")
    print(f"{'='*70}\n")

    last_row = df.iloc[-1]
    print(f"  Latest Close:  ${last_row['close']:.2f}")
    print(f"  RSI(14):       {last_row['rsi']:.1f}" if not pd.isna(last_row.get("rsi")) else "  RSI: N/A")
    print(f"  MACD Line:     {last_row['macd_line']:.2f}" if not pd.isna(last_row.get("macd_line")) else "  MACD: N/A")
    print(f"  MACD Signal:   {last_row['macd_signal']:.2f}" if not pd.isna(last_row.get("macd_signal")) else "  MACD Sig: N/A")
    print(f"  BB Upper:      ${last_row['bb_upper']:.2f}" if not pd.isna(last_row.get("bb_upper")) else "  BB Upper: N/A")
    print(f"  BB Lower:      ${last_row['bb_lower']:.2f}" if not pd.isna(last_row.get("bb_lower")) else "  BB Lower: N/A")

    print(f"\n  Alert Scan ({len(df)} bars):")
    alert_count = 0
    for idx, row in df.iterrows():
        new_alerts = alerts.evaluate(symbol, row)
        alert_count += len(new_alerts)

    print(f"  Total alerts triggered: {alert_count}")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Market Data Pipeline")
    parser.add_argument("--symbol", default="BTCUSDT", help="Trading pair or symbol")
    parser.add_argument("--interval", default="1m", help="Timeframe (1m, 5m, 1h, 1d)")
    parser.add_argument("--mode", choices=["live", "historical"], default="historical",
                        help="Run mode: live (WebSocket) or historical (REST)")
    parser.add_argument("--limit", type=int, default=100, help="Bars to fetch (historical only)")
    parser.add_argument("--source", choices=["binance", "alphavantage"], default="binance")
    parser.add_argument("--apikey", help="API key (Alpha Vantage)")

    args = parser.parse_args()

    if args.mode == "live":
        run_live(symbols=[args.symbol], interval=args.interval)
    else:
        run_historical(args.symbol, args.interval, args.limit)
