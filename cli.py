import argparse
import logging
from src.logging_config import setup_logger
from src.validators import validate_order
from src.market_orders import place_market_order
from src.limit_orders import place_limit_order
from src.advanced.stop_limit import place_stop_limit_order
from src.advanced.oco import place_oco_order
from src.advanced.twap import place_twap_order

setup_logger()

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")

    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True)
    parser.add_argument("--type", required=True)
    parser.add_argument("--quantity", type=float, required=True)
    parser.add_argument("--price", type=float)
    parser.add_argument("--stop_price", type=float, help="Stop price for STOP_LIMIT orders")
    parser.add_argument("--take_profit_price", type=float, help="Take profit price for OCO orders")
    parser.add_argument("--intervals", type=int, help="Number of slices for TWAP")
    parser.add_argument("--interval_seconds", type=int, help="Seconds between TWAP slices")

    args = parser.parse_args()

    try:
        validate_order(
            args.symbol,
            args.side,
            args.type,
            args.quantity,
            args.price,
            args.stop_price
        )

        print("\nOrder Request Summary")
        print("---------------------")
        print(f"Symbol: {args.symbol}")
        print(f"Side:   {args.side}")
        print(f"Type:   {args.type}")
        print(f"Quantity: {args.quantity}")
        if args.price:
            print(f"Price: {args.price}")

        # ── MARKET ──────────────────────────────────────────────────────────
        if args.type.upper() == "MARKET":
            response = place_market_order(
                args.symbol,
                args.side,
                args.quantity
            )
            print("\nOrder Response")
            print("--------------")
            print(f"Order ID:     {response.get('orderId')}")
            print(f"Status:       {response.get('status')}")
            print(f"Executed Qty: {response.get('executedQty')}")
            print(f"Avg Price:    {response.get('avgPrice', 'N/A')}")

        # ── LIMIT ────────────────────────────────────────────────────────────
        elif args.type.upper() == "LIMIT":
            response = place_limit_order(
                args.symbol,
                args.side,
                args.quantity,
                args.price
            )
            print("\nOrder Response")
            print("--------------")
            print(f"Order ID:     {response.get('orderId')}")
            print(f"Status:       {response.get('status')}")
            print(f"Executed Qty: {response.get('executedQty')}")
            print(f"Price:        {args.price}")

        # ── STOP_LIMIT ───────────────────────────────────────────────────────
        elif args.type.upper() == "STOP_LIMIT":
            if not args.stop_price or not args.price:
                raise ValueError("STOP_LIMIT requires --stop_price and --price")
            response = place_stop_limit_order(
                symbol=args.symbol,
                side=args.side,
                quantity=args.quantity,
                stop_price=args.stop_price,
                limit_price=args.price
            )
            print("\nOrder Response")
            print("--------------")
            print(f"Order ID:     {response.get('orderId')}")
            print(f"Status:       {response.get('status')}")
            print(f"Stop Price:   {args.stop_price}")
            print(f"Limit Price:  {args.price}")

        # ── OCO ──────────────────────────────────────────────────────────────
        elif args.type.upper() == "OCO":
            if not args.take_profit_price or not args.stop_price or not args.price:
                raise ValueError("OCO requires --take_profit_price, --stop_price and --price")
            response = place_oco_order(
                symbol=args.symbol,
                side=args.side,
                quantity=args.quantity,
                take_profit_price=args.take_profit_price,
                stop_price=args.stop_price,
                stop_limit_price=args.price
            )
            print("\nOCO Orders placed successfully")
            print("------------------------------")
            print(f"Take-Profit Order ID: {response['take_profit_order'].get('orderId')}")
            print(f"Stop-Loss Order ID:   {response['stop_loss_order'].get('orderId')}")

        # ── TWAP ─────────────────────────────────────────────────────────────
        elif args.type.upper() == "TWAP":
            if not args.intervals or not args.interval_seconds:
                raise ValueError("TWAP requires --intervals and --interval_seconds")
            responses = place_twap_order(
                symbol=args.symbol,
                side=args.side,
                total_quantity=args.quantity,
                intervals=args.intervals,
                interval_seconds=args.interval_seconds
            )
            print(f"\nTWAP Complete — {len(responses)} slices executed")

        # ── UNKNOWN ──────────────────────────────────────────────────────────
        else:
            raise ValueError(f"Unsupported order type: {args.type}")

        print("\n✅ Order placed successfully")

    except Exception as e:
        logging.error(e)
        print(f"\n❌ Order failed: {e}")

if __name__ == "__main__":
    main()


