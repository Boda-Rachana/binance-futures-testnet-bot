# src/advanced/validators.py
def validate_order(symbol, side, order_type, quantity, price=None, stop_price=None):
    if not symbol:
        raise ValueError("Symbol is required")
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")
    if order_type not in ["MARKET", "LIMIT", "STOP_LIMIT", "OCO", "TWAP"]:
        raise ValueError("Order type must be MARKET, LIMIT, or STOP_LIMIT")
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0")
    if order_type == "LIMIT" and price is None:
        raise ValueError("Price is required for LIMIT orders")
    if order_type == "STOP_LIMIT" and (price is None or stop_price is None):
        raise ValueError("Both price and stop_price are required for STOP_LIMIT orders")
