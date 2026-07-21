# Market Data Pipeline

![License](https://img.shields.io/badge/License-MIT-yellow)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)

Real-time market data ingestion, technical analysis, and condition-based alerting system.

## Overview

This project builds a complete data pipeline that connects to real market data sources, computes technical indicators in real-time, and fires alerts when trading conditions are met. It mirrors the kind of infrastructure that quant trading firms run 24/7 to monitor markets and detect opportunities.

### Why a Market Data Pipeline?

Before you can trade, you need data. Before you can backtest, you need historical data. Before you can build strategies, you need to understand market microstructure. This pipeline gives you:

1. **Live data experience** — working with real APIs, rate limits, and streaming data
2. **Feature engineering** — computing indicators that feed into trading models
3. **Operational thinking** — building reliable, restartable, observable systems
4. **Real-time decision logic** — detecting conditions and triggering actions

## Features

- **Live data ingestion** — Binance API (crypto) and Alpha Vantage (stocks)
- **Technical indicators**:
  - RSI (Relative Strength Index) — momentum oscillator (0-100)
  - MACD (Moving Average Convergence Divergence) — trend following
  - Bollinger Bands — volatility-based support/resistance
  - SMA/EMA — simple and exponential moving averages
- **Modular pipeline** — each stage is independent; easy to add new indicators or data sources
- **Alert engine** — configurable conditions that trigger console/dashboard alerts
- **Streaming dashboard** — live terminal-based display updating with each new bar
- **Configuration-driven** — all settings in `config.py`, no hardcoded values

## Project Structure

```
market-data-pipeline/
├── pipeline/
│   ├── __init__.py
│   ├── ingestion.py     # API data fetcher (Binance, Alpha Vantage)
│   ├── indicators.py    # Technical indicators (RSI, MACD, Bollinger, SMA)
│   ├── alerts.py        # Condition evaluation and alert dispatch
│   └── dashboard.py     # Live terminal dashboard display
├── config.py            # Configuration (symbols, intervals, thresholds)
├── pipeline.py          # Main entry point
├── tests/
│   └── test_pipeline.py
├── requirements.txt
└── README.md
```

## How It Works (Step by Step)

### 1. Configuration (`config.py`)

Central configuration defining:
- Data sources (Binance for crypto, Alpha Vantage for equities)
- Symbols to watch (e.g., BTCUSDT, ETHUSDT, AAPL)
- Timeframes (1m, 5m, 1h, 1d)
- Indicator parameters (RSI period, MACD fast/slow/signal, Bollinger std dev)
- Alert thresholds (RSI > 70 overbought, RSI < 30 oversold, Bollinger touch)

### 2. Ingestion (`pipeline/ingestion.py`)

Connects to data sources and fetches OHLCV (Open, High, Low, Close, Volume) bars:

**Binance API** (crypto):
- REST API for historical data
- WebSocket streaming for real-time data
- Handles rate limits and reconnection

**Alpha Vantage** (stocks):
- REST API for daily/intraday data
- API key-based authentication
- CSV or JSON response format

Output: Standardized OHLCV bar dictionary passed to the next pipeline stage.

### 3. Indicators (`pipeline/indicators.py`)

Each bar is passed through the indicator computation stage:

**RSI (Relative Strength Index)**:
```
RSI = 100 - (100 / (1 + RS))
RS = Average Gain (n periods) / Average Loss (n periods)
```
Range: 0-100. Overbought > 70, Oversold < 30.

**MACD (Moving Average Convergence Divergence)**:
```
MACD Line = EMA(12) - EMA(26)
Signal Line = EMA(9) of MACD Line
Histogram = MACD Line - Signal Line
```
Bullish when MACD crosses above Signal. Bearish when below.

**Bollinger Bands**:
```
Middle Band = SMA(20)
Upper Band = SMA(20) + 2 × σ(20)
Lower Band = SMA(20) - 2 × σ(20)
```
Price touching upper band = overextended. Touching lower band = potential reversal.

**SMA/EMA**: Simple and exponential moving averages of configurable periods.

### 4. Alerts (`pipeline/alerts.py`)

Evaluates conditions against the latest indicator values:

```
Conditions {
  "BTCUSDT": {
    "rsi_oversold":   {"indicator": "rsi", "op": "<",  "threshold": 30},
    "rsi_overbought": {"indicator": "rsi", "op": ">",  "threshold": 70},
    "bb_touch_upper": {"indicator": "bb_upper", "op": "crossed_above", "field": "close"},
    "bb_touch_lower": {"indicator": "bb_lower", "op": "crossed_below", "field": "close"},
    "macd_cross":     {"indicator": "macd", "op": "crossed_above", "field": "signal"},
  }
}
```

When a condition triggers, the alert fires to:
- Console (stdout with timestamps and colors)
- Log file (for historical review)
- Dashboard (live terminal display)

### 5. Dashboard (`pipeline/dashboard.py`)

Terminal-based live display that updates with each new bar:

```
┌─────────────────────────────────────────────────────────────┐
│                    MARKET DATA PIPELINE                      │
│                    Live: BTCUSDT (1m)                        │
├──────────┬──────────┬──────────┬──────────┬─────────────────┤
│ Time     │ Price    │ RSI      │ MACD     │ Bollinger       │
├──────────┼──────────┼──────────┼──────────┼─────────────────┤
│ 10:01:00 │ 67,432   │ 62.4     │ +142.3   │ UB: 68,100      │
│ 10:02:00 │ 67,389   │ 58.7     │ +138.1   │ MB: 67,200      │
│ 10:03:00 │ 67,521   │ 65.2     │ +145.6   │ LB: 66,300      │
├──────────┴──────────┴──────────┴──────────┴─────────────────┤
│ Alerts:                                                      │
│ [10:02:15] BTCUSDT — MACD bullish cross                      │
└─────────────────────────────────────────────────────────────┘
```

### 6. Pipeline Runner (`pipeline.py`)

Main entry point that wires everything together:

```
ingestion → indicators → alerts → dashboard
     ↑                          │
     └──────────────────────────┘ (loop)
```

## Example Alert Output

```
[10:02:15] ALERT  [BTCUSDT] MACD bullish cross — MACD line crossed above signal line
[10:05:30] ALERT  [ETHUSDT] RSI oversold — RSI(14) = 28.3 (threshold: 30)
[10:07:42] ALERT  [BTCUSDT] Bollinger Band touch — price touched lower band
```

## Getting Started

```bash
pip install -r requirements.txt
python pipeline.py --symbol BTCUSDT --interval 1m
```

For stock data (requires free API key):
```bash
python pipeline.py --symbol AAPL --source alphavantage --apikey YOUR_KEY
```

## Why This Matters for Quant Trading

This project proves you can:
- **Handle real data** — not just textbook CSV files, but live streaming market data
- **Build operational systems** — pipelines that run reliably, reconnect on failure, and log everything
- **Compute indicators correctly** — matching production implementations from TA-Lib
- **React in real-time** — detecting conditions and triggering actions, just like a trading system
- **Write modular Python** — clean separation of concerns, configuration-driven design

Every quant trading desk runs monitoring pipelines. This project shows you can build one.
