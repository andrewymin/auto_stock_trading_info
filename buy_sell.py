from dates_time import TimeOfDate
import json
from time import sleep


# putting (TimeOfDate) into this class for it to inherit all its attributes and methods
class BuySell(TimeOfDate):

    def __init__(self, macd_json, rsi_json, stock_data):
        # just need the super().__init__() once under the def __init__
        super().__init__()

        self.macd_data = macd_json
        self.rsi_data = rsi_json
        self.stock_data = stock_data

        self.slope = 0

        self.bought = bool(0)
        self.funds = 5000
        self.stocks_held = 0
        self.rsi_69 = bool(0)

# bool(0) is False bool(1) is True

    def slope_calc(self, macd_hist_previous, current_macd_hist):
        """"calculates the slope of the macd hist. from previous to current macd_hist"""
        # m = (y2 - y1) / (x2 - x1) where (x2 - x1) will always equal -1 in this case
        self.slope = (macd_hist_previous - current_macd_hist) / -1
        # print(self.slope)
        return self.slope

    def buy_or_sell(self):
        """Gets macd_data passed through data variable to check if the macd line is higher than the signal line """
        # print(self.stock_data[self.today_date])
        current_macd_hist = float(self.macd_data[self.today_date]["MACD_Hist"])
        macd_hist_previous = float(self.macd_data[self.yesterday_stock_date]["MACD_Hist"])
        macd_hist_current = float(self.macd_data[self.today_date]["MACD_Hist"])

        closing_price = float(self.stock_data[self.today_date]["4. close"])

        # Current today_date rsi
        rsi_today = float(self.rsi_data[self.today_date]["RSI"])

        if not self.rsi_69:
            if not self.bought:
                # if float(data[self.today_date]["MACD_Signal"]) < float(data[self.today_date]["MACD"]):
                if 0.05 < current_macd_hist <= 0.21 and self.slope_calc(current_macd_hist=macd_hist_current,
                                                                        macd_hist_previous=macd_hist_previous) > 0:

                    self.stocks_held = round(self.funds / closing_price)
                    self.funds = round(self.funds % closing_price, 2)
                    self.bought = bool(1)

                    # print(f"This is remaining funds after buying {self.funds}, should be 33.55")
                    # print(self.stocks_held)
                    print(self.today_date)
                    print("Just bought stocks")
                else:
                    # Bought is False thus don't buy and change ticker to new ticker

                    pass
            else:
                # Some bought is True, thus check to see if we need to sell
                if rsi_today > 69.00:
                    self.sell_stocks(closing_price)
                    self.rsi_69 = bool(1)

                    print(self.today_date)
                    print("just sold stocks after rsi > 69")

                elif 0.05 > current_macd_hist or current_macd_hist > 0.50:
                    self.sell_stocks(closing_price)

                    print(self.today_date)
                    print("sold stocks")
                else:
                    # print(current_macd_hist)
                    print("don't sell")
        else:
            if rsi_today <= 60.00:
                self.rsi_69 = bool(0)

    def sell_stocks(self, closing):
        """If macd line is below the signal line sell"""
        # profit = round(money["stocks"] * float(self.stock_data[self.today_date]["4. close"]), 2)
        profit = round(self.stocks_held * closing, 2)
        # print(f"this is profit {profit}, should be 377.7 from 366.45")
        self.funds = round(self.funds + profit, 2)
        self.bought = bool(0)
        self.stocks_held = 0
        # print(f"this is funds after selling {self.funds}, at this point it should be 411.25")
        self.account()

    def account(self):
        money_info = {
            "funds": round(self.funds, 2),
            "bought": self.bought,
            "stocks": self.stocks_held,
        }
        with open("money.json", "w") as new_data:
            json.dump(money_info, new_data, indent=4)
        print("Account updated!")
        # sleep(3)

    def days_for_strat(self, starting_date=None, yesterday_date=None):
        # If starting_date and yesterday_date is NOT given as a argument than the code will run on the current day it is
        # Run (will use DEFAULT VALUE for self.today_date and self.yesterday_stock_date in dates_time.py)
        if starting_date is None and yesterday_date is None:
            self.today_date = self.today_date
            self.yesterday_stock_date = self.yesterday_stock_date
        else:
            # If starting_date and yesterday_date is given as an argument than the code will run what dates are inputed
            # as arguments (Only will be used for testing strategies)
            self.today_date = starting_date
            self.yesterday_stock_date = yesterday_date

