# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
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



# can optimize further by saying if current price is not close to previous high or low
# then check every 30 seconds or min instead of checking constantly

pair_list = ["GBP_AUD", "NAS100_USD"]
orderlist = Other.fetchjson("order")
rev = 0

while True:
    for i in ordderlist:
        Trend.dumphist(i, "M30")
        #Trend.dumpcur(i)
        Order.buyorsellnew(i)
        
#         rev = Order.watch(rev, pair_list)
#         print("still running", rev)

#
# Trend.dumphist("GBP_AUD", "M30")
# data = Other.fetchjson("his")
# result = Trend.overall()
# highandlow = result[2]
#
# curfile = Other.fetchjson("cur")
# bid = float(curfile["prices"][0]["bids"][0]["price"])
# asks = float(curfile["prices"][0]["asks"][0]["price"])
# prehigh = highandlow[-1][0]
# prelow = highandlow[-1][1]
#
# print(prehigh)
# print(bid)
# Order.buyorsell()

#print(data["prices"][0]["bids"])
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
