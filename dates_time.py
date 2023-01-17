import datetime as dt

# change the PAST_RANGE to 150 after testing is complete for 5 months data (stock_data only has 100 data points = 150)
# PAST_RANGE = 11
PAST_RANGE = 150


class TimeOfDate:
    def __init__(self):
        self.today = dt.datetime.now()
        self.day_now = self.today.strftime("%a")
        self.today_hour = int(self.today.strftime("%H"))
        # If run on a SATURDAY than start on FRIDAY which is the last day of open market
        if self.day_now == "Sat":
            self.stock_day = self.today - dt.timedelta(days=1)
            self.today_date = self.stock_day.strftime("%Y-%m-%d")
            self.yesterday_stock_date = self.stock_day - dt.timedelta(days=1)
        # If run on a SUNDAY than start on FRIDAY which is the last day of open market
        elif self.day_now == "Sun":
            self.stock_day = self.today - dt.timedelta(days=2)
            self.today_date = self.stock_day.strftime("%Y-%m-%d")
            self.yesterday_stock_date = self.stock_day - dt.timedelta(days=1)
        # If run on a MONDAY and DURING MARKET OPEN HOURS than start on FRIDAY which is the last day of open market
        elif self.day_now == "Mon" and self.today_hour < 14:
            self.stock_day = self.today - dt.timedelta(days=3)
            self.today_date = self.stock_day.strftime("%Y-%m-%d")
            self.yesterday_stock_date = self.stock_day - dt.timedelta(days=1)
        # If run on a MONDAY and AFTER MARKET OPEN HOURS than start on CURRENT day
        elif self.day_now == "Mon" and self.today_hour >= 14:
            self.today_date = self.today.strftime("%Y-%m-%d")
            self.yesterday_stock_date = (self.today - dt.timedelta(days=3)).strftime("%Y-%m-%d")
        # If run on a Tuesday and DURING MARKET OPEN HOURS than start on PREVIOUS day with yesterday as FRIDAY
        elif self.day_now == "Tue" and self.today_hour < 14:
            self.stock_day = self.today - dt.timedelta(days=1)
            self.today_date = self.stock_day.strftime("%Y-%m-%d")
            self.yesterday_stock_date = self.stock_day - dt.timedelta(days=3)
        # If run on a WEEKDAY and DURING MARKET OPEN HOURS than start on PREVIOUS day
        elif self.today_hour < 14:
            self.stock_day = self.today - dt.timedelta(days=1)
            self.today_date = self.stock_day.strftime("%Y-%m-%d")
            self.yesterday_stock_date = self.stock_day - dt.timedelta(days=1)
        else:
            # If run AFTER market is CLOSED
            self.today_date = self.today.strftime("%Y-%m-%d")
        # Constant used for calculating slope of current macd hist.
            self.yesterday_stock_date = (self.today - dt.timedelta(days=1)).strftime("%Y-%m-%d")

    def test_strategies_days(self):
        """Returns the previous dates from today's date specified from the range that is set"""
        # previous_days = [(self.today - dt.timedelta(days=days_past)).strftime("%Y-%m-%d")
        #                  for days_past in range(1, 181)]
        # 181 is used for 30*6 for 6 months back test
        previous_days = []
        for days_past in range(0, PAST_RANGE):
            past_day = self.today - dt.timedelta(days=days_past)
            if past_day.strftime("%a") == "Sat" or past_day.strftime("%a") == "Sun":
                continue
            else:
                previous_days.append(past_day.strftime("%Y-%m-%d"))
        # reversed the dates to oldest to newest using slicing of [::-1]
        return previous_days[::-1]


# test_day = TimeOfDate()
#
#
# reversed_days = test_day.test_strategies_days()
# print(reversed_days)
# print(len(reversed_days))
# current_day_list = reversed_days[1:]
# yesterday_list = reversed_days[:-1]
# for i in range(len(reversed_days) - 1):
#     print(current_day_list[i])
#     print(yesterday_list[i])
#     print("")

