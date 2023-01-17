import json
import os
import time

from dotenv import load_dotenv
import requests

load_dotenv("C:/Users/krazy/Desktop/Code/.env.txt")
STOCK_DATA_KEY = os.getenv("api_key_stock_data")
# STOCK_NAME = "Chase Corporation"
DATA_URL = "https://www.alphavantage.co/query?"
INTERVAL = "daily"


class Indicators:
    def __init__(self):
        self.macd_params = {}
        self.rsi_params = {}
        self.macd_data = {}
        self.rsi_data = {}

    def macd_indicator(self, ticker):
        self.macd_params = {
            "function": "MACD",
            "symbol": ticker,
            "interval": INTERVAL,
            "series_type": "close",
            "fastperiod": 8,
            "slowperiod": 21,
            "signalperiod": 5,
            "apikey": STOCK_DATA_KEY,
        }

        response = requests.get(DATA_URL, params=self.macd_params)
        response.raise_for_status()
        macd_data = response.json()["Technical Analysis: MACD"]
        # with open("macd_data.json", "w") as data_file:
        #     json.dump(macd_data, data_file, indent=4)
        time.sleep(3)
        self.macd_data = macd_data
        return macd_data

    def rsi_indicator(self, ticker):
        self.rsi_params = {
            "function": "RSI",
            "symbol": ticker,
            "interval": INTERVAL,
            "series_type": "close",
            "time_period": 14,
            "apikey": STOCK_DATA_KEY,
        }

        response = requests.get(DATA_URL, params=self.rsi_params)
        response.raise_for_status()
        time.sleep(3)
        rsi_data = response.json()["Technical Analysis: RSI"]
        # with open("rsi_data.json", "w") as data_file:
        #     json.dump(rsi_data, data_file, indent=4)
        self.rsi_data = rsi_data
        return rsi_data

    def bb_indicator(self):
        pass
