# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import json
import oandapyV20
from oandapyV20 import API
from oandapyV20.exceptions import V20Error
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.pricing as pricing
from oandapyV20.contrib.factories import InstrumentsCandlesFactory
import datetime
from datetime import datetime, timedelta
import Trend
import Other
import Order

# data = [1, 2, 3, 4, 5, 6]
# with open("Historicaldata.json", "w") as out:
#     out.write(json.dumps(data, indent = 4))
# with open("Historicaldata.json", "r") as read:
#     print(json.load(read))

while True:
    Trend.dumphist("GBP_AUD", "M30")
    Trend.dumpcur("GBP_AUD")
    orderlist = Order.buyorsell()
    Order.watch(orderlist)
    print(orderlist)




# for i in data:
#     print(i["time"])
#     result = trendassign(i)
#     print(result[0])
#     print(result[1])
#dumphist("CAD_JPY", "M30")


#Trend.dumphist("GBP_AUD", "M30")
# listolist = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# print(listolist)
# i = 0
# del listolist[i]
# print(listolist)
#
# lowest = float(data[length]["mid"]["c"])
# highest = float(data[length]["mid"]["c"])
# lowestwick = float(data[length]["mid"]["c"])
# highestwick = float(data[length]["mid"]["c"])
# for i in range(length, -1, -1):
#     if highest < float(data[i]["mid"]["c"]):
#         highest = float(data[i]["mid"]["c"])
#     if lowest > float(data[i]["mid"]["c"]):
#         lowest = float(data[i]["mid"]["c"])
#     if lowestwick > float(data[i]["mid"]["l"]):
#         lowestwick = float(data[i]["mid"]["l"])
#     if highestwick < float(data[i]["mid"]["h"]):
#         highestwick = float(data[i]["mid"]["h"])
#
# print(highestwick)
# print(highest)
# print(lowestwick)
# print(lowest)
#print(data["prices"][0]["bids"])
# See PyCharm help at https://www.jetbrains.com/help/pycharm/