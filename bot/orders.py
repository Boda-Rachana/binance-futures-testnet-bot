from bot.client import BinanceFuturesClient

def create_order(symbol, side, order_type, quantity, price=None):
    client = BinanceFuturesClient()

    order_data = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity
    }

    if order_type == "LIMIT":
        order_data["price"] = price
        order_data["timeInForce"] = "GTC"

    return client.place_order(**order_data)
