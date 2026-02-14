import logging
import time
from src.client import BinanceFuturesClient

# src/advanced/grid_strategy.py

def place_grid_orders(symbol, quantity_per_grid, lower_price, upper_price, grid_levels):
    """
    Executes a Grid Trading strategy on Binance Futures Testnet.

    Places alternating BUY limit orders below current price and SELL limit
    orders above current price across evenly spaced grid levels.

    Args:
        symbol (str): Trading pair, e.g. "BTCUSDT"
        quantity_per_grid (float): Quantity to trade at each grid level
        lower_price (float): Lowest price in the grid range
        upper_price (float): Highest price in the grid range
        grid_levels (int): Number of grid levels to create

    Returns:
        dict: Contains lists of buy_orders and sell_orders placed
    """
    client = BinanceFuturesClient()

    # Calculate evenly spaced price levels
    step = (upper_price - lower_price) / (grid_levels - 1)
    price_levels = [round(lower_price + i * step, 2) for i in range(grid_levels)]
    mid_price = (upper_price + lower_price) / 2

    buy_orders = []
    sell_orders = []

    logging.info(
        f"Starting Grid: {symbol} | Levels: {grid_levels} | "
        f"Range: {lower_price} - {upper_price} | Step: {step}"
    )

    print(f"\n  Grid Range: {lower_price} → {upper_price}")
    print(f"  Levels: {grid_levels} | Step size: {round(step, 2)}")
    print(f"  Midpoint: {mid_price}\n")

    for price in price_levels:
        if price < mid_price:
            # Place BUY limit order below midpoint
            try:
                response = client.place_order(
                    symbol=symbol,
                    side="BUY",
                    type="LIMIT",
                    quantity=quantity_per_grid,
                    price=str(round(price, 2)),
                    timeInForce="GTC"
                )
                buy_orders.append(response)
                logging.info(f"Grid BUY order placed at {price}: {response}")
                print(f"  ✅ BUY  @ {round(price, 2)} — Order ID: {response.get('orderId')}")
            except Exception as e:
                logging.error(f"Grid BUY order failed at {price}: {e}")
                print(f"  ❌ BUY  @ {round(price, 2)} failed: {e}")

        else:
            # Place SELL limit order above midpoint
            try:
                response = client.place_order(
                    symbol=symbol,
                    side="SELL",
                    type="LIMIT",
                    quantity=quantity_per_grid,
                    price=str(round(price, 2)),
                    timeInForce="GTC"
                )
                sell_orders.append(response)
                logging.info(f"Grid SELL order placed at {price}: {response}")
                print(f"  ✅ SELL @ {round(price, 2)} — Order ID: {response.get('orderId')}")
            except Exception as e:
                logging.error(f"Grid SELL order failed at {price}: {e}")
                print(f"  ❌ SELL @ {round(price, 2)} failed: {e}")

        time.sleep(0.3)  # Small delay to avoid rate limiting

    logging.info(
        f"Grid complete. BUY orders: {len(buy_orders)}, SELL orders: {len(sell_orders)}"
    )

    return {
        "buy_orders": buy_orders,
        "sell_orders": sell_orders
    }






