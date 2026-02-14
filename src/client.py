import os
import logging
import time
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()


class BinanceFuturesClient:
    def __init__(self):
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")

        if not api_key or not api_secret:
            raise ValueError("API keys not found. Set BINANCE_API_KEY and BINANCE_API_SECRET")

        self.client = Client(api_key, api_secret)

        # Set Futures Testnet URL
        self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

        # Sync timestamp properly
        server_time = self.client.futures_time()
        local_time = int(time.time() * 1000)
        self.client.timestamp_offset = server_time["serverTime"] - local_time

    def place_order(self, **order_data):
        try:
            logging.info(f"Placing order: {order_data}")
            response = self.client.futures_create_order(**order_data)
            logging.info(f"Order response: {response}")
            return response
        except Exception as e:
            logging.error(f"Order failed: {e}")
            raise
