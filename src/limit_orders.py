from src.client import BinanceFuturesClient

def place_limit_order(symbol, side, quantity, price):
    client = BinanceFuturesClient()

    return client.place_order(
        symbol=symbol,
        side=side,
        type="LIMIT",
        quantity=quantity,
        price=price,
        timeInForce="GTC"
    )
