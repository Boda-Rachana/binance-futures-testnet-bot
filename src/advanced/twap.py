import time
import logging
from src.client import BinanceFuturesClient

# src/advanced/twap.py

def place_twap_order(symbol, side, total_quantity, intervals, interval_seconds):
    """
    Executes a TWAP (Time-Weighted Average Price) strategy on Binance Futures Testnet.

    Splits a large order into equal smaller market orders placed over time
    to minimize market impact.

    Args:
        symbol (str): Trading pair, e.g. "BTCUSDT"
        side (str): "BUY" or "SELL"
        total_quantity (float): Total quantity to trade
        intervals (int): Number of smaller orders to split into
        interval_seconds (int): Seconds to wait between each order

    Returns:
        list: List of all order responses
    """
    client = BinanceFuturesClient()

    slice_quantity = round(total_quantity / intervals, 3)
    responses = []

    logging.info(
        f"Starting TWAP: {symbol} {side} {total_quantity} "
        f"split into {intervals} orders every {interval_seconds}s"
    )

    for i in range(intervals):
        logging.info(f"TWAP slice {i + 1}/{intervals}: placing {slice_quantity} {symbol}")

        response = client.place_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=slice_quantity
        )

        logging.info(f"TWAP slice {i + 1} response: {response}")
        responses.append(response)

        print(f"  ✅ Slice {i + 1}/{intervals} placed — Order ID: {response.get('orderId')}")

        # Wait before next slice (skip waiting after last order)
        if i < intervals - 1:
            time.sleep(interval_seconds)

    logging.info(f"TWAP complete. Total slices executed: {len(responses)}")
    return responses
