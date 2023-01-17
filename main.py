from stock_search import StockSearch
from indicator import Indicators
from buy_sell import BuySell
from dates_time import TimeOfDate
import json

# TODO: Create a way to change stocks if there is no good buy on current stock
# TODO: Add msg or email for when auto_trader does make a buy/sell
# TODO: Add td ameritrade api to trade on my account on my behave

TICKER = "AAPL"
# ticker_symbols = ["AAPL", "NIO", "INTC", "CMCSA"]
# ticker_position = [num]
# num = 0
# add 1 to num when there is no good buy for a change of ticker. If all tickers are no good than end loop.

stock = StockSearch()
stock_data = stock.stock_data(TICKER)
# with open("stock_data.json", "w") as data_file:
#     json.dump(stock_data, data_file, indent=4)

indicator = Indicators()
macd_data = indicator.macd_indicator(TICKER)
# with open("macd_data.json", "w") as data_file:
#     json.dump(macd_data, data_file, indent=4)

rsi_data = indicator.rsi_indicator(TICKER)
# with open("rsi_data.json", "w") as data_file:
#     json.dump(rsi_data, data_file, indent=4)

# # # For current day trading
# # decision = BuySell(macd_json=indicator.macd_data, rsi_json=indicator.rsi_data, stock_data=stock_data)

decision = BuySell(macd_json=indicator.macd_data, rsi_json=indicator.rsi_data, stock_data=stock_data)

# TODO: start test loop of past days here, using inherited class of BuySell
# Using inherited method to get the reversed list of dates 5 months back
test_day = TimeOfDate()

reversed_days = test_day.test_strategies_days()
stock_day_list = reversed_days[1:]
yesterday_list = reversed_days[:-1]

# reversed_days = ['2021-03-30', '2021-03-31', '2021-04-01', '2021-04-05']
# stock_day_list = reversed_days[1:]
# yesterday_list = reversed_days[:-1]

for i in range(len(reversed_days) - 1):
    current_stock_day = stock_day_list[i]
    yesterday_day = yesterday_list[i]
    try:
        decision.days_for_strat(starting_date=current_stock_day, yesterday_date=yesterday_day)
        decision.buy_or_sell()
    except KeyError as error:
        print(f"{error} is probably a holiday.")


