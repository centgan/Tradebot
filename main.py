# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import Connect
import Trend
import Other
import Order
import json
import datetime

# can optimize further by saying if current price is not close to previous high or low
# then check every 30 seconds or min instead of checking constantly


pair_list = ["GBP_AUD", "GBP_USD", "NAS100_USD"]

while True:
    day = datetime.datetime.today().weekday()
    time = datetime.datetime.now().strftime("%H")
    if day == 6 and int(time) >= 17:
        for i in pair_list:
            Trend.dumphist(i, "M30")
            Trend.overall(i)
    elif 0 >= day >= 3:
        for i in pair_list:
            Trend.dumphist(i, "M30")
            Trend.overall(i)
            Order.buyorsellnew(i)
            Order.watchnew(i)
            Connect.db()
            Connect.changes()
    elif day == 4 and int(time) <= 17:
        for i in pair_list:
            Trend.dumphist(i, "M30")
            Trend.overall(i)
            Order.buyorsellnew(i)
            Order.watchnew(i)
            Connect.db()
            Connect.changes()
    elif day == 5:
        pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
