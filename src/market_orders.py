from src.client import BinanceFuturesClient

def place_market_order(symbol, side, quantity):
    client = BinanceFuturesClient()

    return client.place_order(
        symbol=symbol,
        side=side,
        type="MARKET",
        quantity=quantity
    )