import logging
from src.client import BinanceFuturesClient

# src/advanced/oco.py

def place_oco_order(symbol, side, quantity, take_profit_price, stop_price, stop_limit_price):
    """
    Simulates an OCO (One-Cancels-the-Other) order on Binance Futures Testnet.

    Places two orders simultaneously:
      1. A TAKE_PROFIT_MARKET order (closes position when price hits take_profit_price)
      2. A STOP order (stop-loss limit order when price hits stop_price)

    Args:
        symbol (str): Trading pair, e.g. "BTCUSDT"
        side (str): "BUY" or "SELL"
        quantity (float): Quantity to trade
        take_profit_price (float): Price at which to take profit
        stop_price (float): Stop trigger price for the stop-loss
        stop_limit_price (float): Limit price for the stop-loss order

    Returns:
        dict: Contains both order responses
    """
    client = BinanceFuturesClient()

    # Order 1: Take-Profit order
    take_profit_order = client.place_order(
        symbol=symbol,
        side=side,
        type="TAKE_PROFIT_MARKET",
        quantity=quantity,
        stopPrice=str(take_profit_price),
        timeInForce="GTC"
    )
    logging.info(f"OCO Take-Profit order placed: {take_profit_order}")

    # Order 2: Stop-Loss order
    stop_loss_order = client.place_order(
        symbol=symbol,
        side=side,
        type="STOP",
        quantity=quantity,
        price=str(stop_limit_price),
        stopPrice=str(stop_price),
        timeInForce="GTC"
    )
    logging.info(f"OCO Stop-Loss order placed: {stop_loss_order}")

    return {
        "take_profit_order": take_profit_order,
        "stop_loss_order": stop_loss_order
    }
