import numpy as np
import pandas as pd


class TechnicalIndicators:
    def __init__(self, config=None):
        self.config = config or {}

    def compute_all(self, df):
        df = df.copy()
        df = self.rsi(df, period=self.config.get("rsi_period", 14))
        df = self.macd(df, fast=self.config.get("macd_fast", 12),
                        slow=self.config.get("macd_slow", 26),
                        signal=self.config.get("macd_signal", 9))
        df = self.bollinger_bands(df, period=self.config.get("bb_period", 20),
                                  std_dev=self.config.get("bb_std", 2.0))
        for p in self.config.get("sma_periods", [20, 50]):
            df = self.sma(df, period=p)
        for p in self.config.get("ema_periods", [12, 26]):
            df = self.ema(df, period=p)
        return df

    @staticmethod
    def sma(df, period=20):
        df[f"sma_{period}"] = df["close"].rolling(window=period).mean()
        return df

    @staticmethod
    def ema(df, period=12):
        df[f"ema_{period}"] = df["close"].ewm(span=period, adjust=False).mean()
        return df

    @staticmethod
    def rsi(df, period=14):
        delta = df["close"].diff()
        gain = delta.where(delta > 0, 0.0)
        loss = (-delta).where(delta < 0, 0.0)
        avg_gain = gain.ewm(span=period, adjust=False).mean()
        avg_loss = loss.ewm(span=period, adjust=False).mean()
        rs = avg_gain / avg_loss.replace(0, np.nan)
        df["rsi"] = 100 - (100 / (1 + rs))
        df["rsi"] = df["rsi"].fillna(50)
        return df

    @staticmethod
    def macd(df, fast=12, slow=26, signal=9):
        ema_fast = df["close"].ewm(span=fast, adjust=False).mean()
        ema_slow = df["close"].ewm(span=slow, adjust=False).mean()
        df["macd_line"] = ema_fast - ema_slow
        df["macd_signal"] = df["macd_line"].ewm(span=signal, adjust=False).mean()
        df["macd_histogram"] = df["macd_line"] - df["macd_signal"]
        return df

    @staticmethod
    def bollinger_bands(df, period=20, std_dev=2.0):
        df["bb_middle"] = df["close"].rolling(window=period).mean()
        bb_std = df["close"].rolling(window=period).std()
        df["bb_upper"] = df["bb_middle"] + std_dev * bb_std
        df["bb_lower"] = df["bb_middle"] - std_dev * bb_std
        df["bb_width"] = (df["bb_upper"] - df["bb_lower"]) / df["bb_middle"]
        df["bb_position"] = (df["close"] - df["bb_lower"]) / (df["bb_upper"] - df["bb_lower"])
        return df

    @staticmethod
    def atr(df, period=14):
        high, low, close = df["high"], df["low"], df["close"]
        tr = pd.concat([
            high - low,
            (high - close.shift()).abs(),
            (low - close.shift()).abs()
        ], axis=1).max(axis=1)
        df["atr"] = tr.rolling(window=period).mean()
        return df
