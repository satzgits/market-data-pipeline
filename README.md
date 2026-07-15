# Market Data Pipeline

Real-time market data ingestion, technical analysis, and alerting system.

## Features

- Pulls live crypto/stock data via Binance API or Alpha Vantage
- Computes technical indicators: RSI, MACD, Bollinger Bands
- Streams to console dashboard or logs alerts on condition triggers
- Modular pipeline architecture — easy to add new indicators or data sources

## Motivation

Quant trading requires real-time data handling. This pipeline shows you can build the infrastructure to ingest, process, and act on market data.

## Getting Started

```bash
pip install -r requirements.txt
python pipeline.py --symbol BTCUSDT --interval 1m
```

## Project Structure

```
├── pipeline/
│   ├── ingestion.py     # API data fetcher
│   ├── indicators.py    # Technical indicators
│   ├── alerts.py        # Condition-based alerts
│   └── dashboard.py     # Streaming display
├── config.py
├── pipeline.py          # Main entry point
├── tests/
├── requirements.txt
└── README.md
```

## Example Alert

```
[ALERT] BTCUSDT — RSI(14) = 28.3 (oversold)
[ALERT] BTCUSDT — Bollinger Band touch (lower)
```
