import logging
from datetime import datetime


class AlertEngine:
    def __init__(self, thresholds=None):
        self.thresholds = thresholds or {
            "rsi_oversold": 30,
            "rsi_overbought": 70,
        }
        self.alerts = []
        self._setup_logging()

    def _setup_logging(self):
        self.logger = logging.getLogger("MarketDataPipeline")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s",
                datefmt="%H:%M:%S"
            ))
            self.logger.addHandler(handler)
            file_handler = logging.FileHandler("pipeline.log")
            file_handler.setFormatter(logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s"
            ))
            self.logger.addHandler(file_handler)

    def evaluate(self, symbol, row):
        alerts = []

        if not pd.isna(row.get("rsi")):
            if row["rsi"] < self.thresholds["rsi_oversold"]:
                msg = f"[{symbol}] RSI oversold — RSI(14) = {row['rsi']:.1f} (threshold: {self.thresholds['rsi_oversold']})"
                alerts.append(("RSI_OVERSOLD", msg))
            elif row["rsi"] > self.thresholds["rsi_overbought"]:
                msg = f"[{symbol}] RSI overbought — RSI(14) = {row['rsi']:.1f} (threshold: {self.thresholds['rsi_overbought']})"
                alerts.append(("RSI_OVERBOUGHT", msg))

        if not pd.isna(row.get("macd_line")) and not pd.isna(row.get("macd_signal")):
            macd_diff = row["macd_line"] - row["macd_signal"]
            if abs(macd_diff) < 0.1 * abs(row["macd_line"]):
                alerts.append(("MACD_CROSS", f"[{symbol}] MACD approaching signal line — possible cross"))

        if not pd.isna(row.get("bb_lower")) and not pd.isna(row.get("close")):
            if row["close"] <= row["bb_lower"] * 1.005:
                alerts.append(("BB_LOWER_TOUCH", f"[{symbol}] Price at lower Bollinger Band — ${row['close']:.2f}"))
            elif row["close"] >= row["bb_upper"] * 0.995:
                alerts.append(("BB_UPPER_TOUCH", f"[{symbol}] Price at upper Bollinger Band — ${row['close']:.2f}"))

        for alert_type, msg in alerts:
            self.logger.warning(msg)
            self.alerts.append({
                "time": datetime.now(),
                "symbol": symbol,
                "type": alert_type,
                "message": msg
            })

        return alerts
