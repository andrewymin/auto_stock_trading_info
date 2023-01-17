import json
import time
from time import sleep
import os
from dotenv import load_dotenv
import requests

load_dotenv("C:/Users/krazy/Desktop/Code/.env.txt")
STOCK_DATA_KEY = os.getenv("api_key_stock_data")
# STOCK_NAME = "Chase Corporation"
DATA_URL = "https://www.alphavantage.co/query?"
# INTERVAL = "30min"


class StockSearch:
    def __init__(self):
        self.data_params = {}

    def stock_data(self, ticker):
        self.data_params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": ticker,
            # "interval": INTERVAL,
            "apikey": STOCK_DATA_KEY,
        }

        response = requests.get(DATA_URL, params=self.data_params)
        response.raise_for_status()
        # stock_data = response.json()[f"Time Series ({self.data_params['interval']})"]
        time.sleep(3)
        stock_data = response.json()["Time Series (Daily)"]
        return stock_data

        # with open("stock_data.json", "w") as data_file:
        #     json.dump(stock_data, data_file, indent=4)

    def loop_through_tickers(self):
        pass
