# Binance Futures Testnet Trading Bot

## Overview
A simplified Python trading bot that places MARKET and LIMIT orders on Binance Futures Testnet (USDT-M) using a CLI interface.

## Features
- Place MARKET and LIMIT orders
- Supports BUY and SELL
- Command-line interface using argparse
- Input validation
- Structured logging
- Error handling for API and network errors

## Setup Instructions

1. Clone the repository / unzip the project
2. Create virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
3.Install dependencies:
   pip install -r requirements.txt
4.Set Binance Testnet API credentials as environment variables:
   export BINANCE_API_KEY=your_key
   export BINANCE_API_SECRET=your_secret
# How to Run
# Market Order
python cli.py --symbol BTCUSDT --side SELL --type MARKET --quantity 0.002
# Limit Order
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.002 --price 60000
# Logs
All API requests, responses, and errors are logged to:
    logs/trading.log
# Assumptions
- USDT-M Futures Testnet is used
- Minimum notional requirements apply as per Binance rules
