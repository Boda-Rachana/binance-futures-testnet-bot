import logging
from src.client import BinanceFuturesClient
def place_stop_limit_order(symbol, side, quantity, stop_price, limit_price):
    """
    Places a STOP_LIMIT order on Binance Futures Testnet.

    Args:
        symbol (str): Trading pair, e.g. "BTCUSDT"
        side (str): "BUY" or "SELL"
        quantity (float): Quantity to trade
        stop_price (float): Price that triggers the order
        limit_price (float): Limit price for the order once triggered

    Returns:
        dict: Binance API response
    """
    client = BinanceFuturesClient()

    order_data = {
        "symbol": symbol,
        "side": side,
        "type": "STOP",
        "quantity": quantity,
        "price": str(limit_price),
        "stopPrice": str(stop_price),
        "timeInForce": "GTC"
    }
    return client.place_order(**order_data)