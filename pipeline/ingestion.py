import requests
import pandas as pd
import time
import json
from datetime import datetime


class DataIngestion:
    def __init__(self):
        self.sources = {}

    def fetch_binance_klines(self, symbol="BTCUSDT", interval="1m", limit=100):
        url = f"https://api.binance.com/api/v3/klines"
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        bars = []
        for k in data:
            bars.append({
                "timestamp": datetime.fromtimestamp(k[0] / 1000),
                "open": float(k[1]),
                "high": float(k[2]),
                "low": float(k[3]),
                "close": float(k[4]),
                "volume": float(k[5]),
            })

        return pd.DataFrame(bars).set_index("timestamp")

    def fetch_alphavantage(self, symbol="AAPL", interval="5min", apikey="demo"):
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": interval,
            "apikey": apikey,
            "outputsize": "compact",
        }
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        key = f"Time Series ({interval})"
        if key not in data:
            raise ValueError(f"Alpha Vantage error: {data.get('Note', data)}")

        records = []
        for ts, values in data[key].items():
            records.append({
                "timestamp": pd.Timestamp(ts),
                "open": float(values["1. open"]),
                "high": float(values["2. high"]),
                "low": float(values["3. low"]),
                "close": float(values["4. close"]),
                "volume": float(values["5. volume"]),
            })

        df = pd.DataFrame(records).set_index("timestamp")
        df = df.sort_index()
        return df

    @staticmethod
    def stream_binance_websocket(symbols, callback, interval="1m"):
        import websocket
        import threading

        streams = "/".join([f"{s.lower()}@kline_{interval}" for s in symbols])
        url = f"wss://stream.binance.com:9443/stream?streams={streams}"

        def on_message(ws, message):
            data = json.loads(message)
            if "data" in data:
                k = data["data"]["k"]
                bar = {
                    "timestamp": datetime.fromtimestamp(k["t"] / 1000),
                    "symbol": data["data"]["s"],
                    "open": float(k["o"]),
                    "high": float(k["h"]),
                    "low": float(k["l"]),
                    "close": float(k["c"]),
                    "volume": float(k["v"]),
                    "is_final": k["x"],
                }
                callback(bar)

        def on_error(ws, error):
            print(f"WebSocket error: {error}")

        def on_close(ws, close_status_code, close_msg):
            print("WebSocket closed. Reconnecting in 5s...")
            time.sleep(5)
            ws.run_forever()

        ws = websocket.WebSocketApp(url, on_message=on_message, on_error=on_error, on_close=on_close)
        thread = threading.Thread(target=ws.run_forever, daemon=True)
        thread.start()
        return ws
