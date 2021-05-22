import Trend
import Other

#The information here is for current price
def stoploss(sellorbuy):
    data = Other.fetchjson("his")
    now = data[-1]
    if sellorbuy == "buy":
        sl = now["mid"]["l"]
        return sl
    elif sellorbuy == "sell":
        sl = now["mid"]["h"]
        return sl

def takeprofit(sellorbuy, cur):
    if sellorbuy == "sell":
        cur = float(cur) - 0.0025
        return cur
    elif sellorbuy == "buy":
        cur = float(cur) + 0.0025
        return cur

def watch(orderlist):
    datahis = Other.fetchjson("his")
    cur = datahis[-1]
    curfile = Other.fetchjson("cur")
    bid = float(curfile["prices"][0]["bids"][0]["price"])
    asks = float(curfile["prices"][0]["asks"][0]["price"])
    for i in orderlist:
        if "buy" in i[0]:
            halfstopprep = (float(i[1]) - float(i[2])) / 2
            halfstop = float(i[1]) - halfstopprep
            uphalfprep = (float(i[3]) - float(i[1])) / 2
            uphalf = float(i[1]) + uphalfprep
            if bid <= halfstop:
                print("close half positions because of stop loss", i)
                if bid <= i[1]:
                    print("add back to the position")
            elif bid >= uphalf:
                print("close half positions because of tp and move sl to 10 pips", i)
            elif bid >= float(i[3]):
                print("take profit full profits", i)
            elif bid <= float(i[2]):
                print("hit full stop loss", i)
            elif cur["complete"] == "true" and cur["color"] == "red" and datahis[-2]["color"] == "red":
                print("closed in prediction of a reversal")
        elif "sell" in i[0]:
            halfstopprep = (float(i[2]) - float(i[1])) / 2
            halfstop = float(i[1]) + halfstopprep
            uphalfprep = (float(i[1]) - float(i[3])) / 2
            uphalf = float(i[1]) - uphalfprep
            if asks >= halfstop:
                print("close half positions because of stop loss", i)
                if asks <= i[1]:
                    print("add back to the position")
            elif asks <= uphalf:
                print("close half positions because of tp and move sl to 10 pips", i)
            elif asks <= float(i[3]):
                print("take profit full profits", i)
            elif asks >= float(i[2]):
                print("hit full stop loss", i)
            elif cur["complete"] == "true" and cur["color"] == "green" and datahis[-2]["color"] == "green":
                print("closed in prediction of a reversal")

## READ ME ##
## first we need to get it so that only the order is only put in once think about
# possible adding in another item in the list that says complete or executed##
## next we need to add a function that adds back to the positions
# so if hit the half way mark in the stop loss but reverses back to the open price
# the we add back to the position ensuring that we make more profit##

orderlist = []
def buyorsell():
    result = Trend.overall()
    zone = result[0]
    order = result[1]
    highandlow = result[2]

    datahis = Other.fetchjson("his")
    cur = datahis[-1]
    curfile = Other.fetchjson("cur")
    bid = float(curfile["prices"][0]["bids"][0]["price"])
    asks = float(curfile["prices"][0]["asks"][0]["price"])
    prehigh = highandlow[-1][0]
    prelow = highandlow[-1][1]
    # pre = data[-2]
    if float(cur["mid"]["c"]) > float(prehigh):
        #other.timecheck results in the time remaining NOT the time it has taken
        sl = stoploss("buy")
        if 12 < Other.timecheck("forward") <= 15:
            Trend.lower("M15", "GBP_AUD")
            data = Other.fetchjson("lower")
            if len(orderlist) == 0 and data[-2]["mid"]["c"] > prehigh:
                orderlist.append(["buy m15 close", bid, sl, takeprofit("buy", cur["mid"]["c"]), prehigh, data[-2]["time"]])
                print("enter buy  m15 close with sl at", sl)
            elif data[-2]["mid"]["c"] > prehigh and prehigh != orderlist[-1][4]:#and str(prehigh) != orderlist[-1][4]:
                orderlist.append(["buy m15 close", bid, sl, takeprofit("buy", cur["mid"]["c"]), prehigh, data[-2]["time"]])
                print("enter buy  m15 close with sl at", sl)
        #5min close will have be modified later
        elif 3 < Other.timecheck("forward") < 10:
            Trend.lower("M5", "GBP_AUD")
            data = Other.fetchjson("lower")
            if len(orderlist) == 0 and data[-2]["mid"]["c"] > prehigh:
                orderlist.append(["buy m5 close", bid, sl, takeprofit("buy", cur["mid"]["c"]), prehigh, data[-2]["time"]])
                print("enter buy  m15 close with sl at", sl)
            elif data[-2]["mid"]["c"] > prehigh and prehigh != orderlist[-1][4]:#prehigh not in orderlist[-1]:
                orderlist.append(["buy m5 close", bid, sl, takeprofit("buy", cur["mid"]["c"]), prehigh, data[-2]["time"]])
                print("enter buy m5 close with sl at", sl)
        elif Other.timecheck("forward") < 3:
            result = Other.fetchjson("his")
            data = result[-1]["time"]
            if len(orderlist) == 0:
                orderlist.append(["buy m30 close", bid, sl, takeprofit("buy", cur["mid"]["c"]), prehigh, data[-2]["time"]])
                print("enter buy m30 close with sl at", sl)
            elif prehigh != orderlist[-1][4]:
                orderlist.append(["buy m30 close", bid, sl, takeprofit("buy", cur["mid"]["c"]), prehigh, data[-2]["time"]])
                print("enter buy m30 close with sl at", sl)
    elif float(cur["mid"]["c"]) < float(prelow):
        sl = stoploss("sell")
        if 12 < Other.timecheck("forward") <= 15:
            Trend.lower("M15", "GBP_AUD")
            data = Other.fetchjson("lower")
            if len(orderlist) == 0 and data[0]["mid"]["c"] < prelow:
                orderlist.append(["sell m15 close", asks, sl, takeprofit("sell", cur["mid"]["c"]), prelow, data[-2]["time"]])
                print("enter sell m15 close with sl at", sl)
            elif data[0]["mid"]["c"] < prelow and prelow != orderlist[-1][4]:#prelow not in orderlist[-1]:
                orderlist.append(["sell m15 close", asks, sl, takeprofit("sell", cur["mid"]["c"]), prelow, data[-2]["time"]])
                print("enter sell  m15 close with sl at", sl)
        elif 3 < Other.timecheck("forward") < 8:
            Trend.lower("M5", "GBP_AUD")
            data = Other.fetchjson("lower")
            if len(orderlist) == 0 and data[0]["mid"]["c"] < prelow:
                orderlist.append(["sell m5 close", asks, sl, takeprofit("sell", cur["mid"]["c"]), prelow, data[-2]["time"]])
                print("enter sell m5 close with sl at", sl)
            elif data[-2]["mid"]["c"] < prelow and prelow != orderlist[-1][4]:#prelow not in orderlist[-1]:
                orderlist.append(["sell m5 close", asks, sl, takeprofit("sell", cur["mid"]["c"]), prelow, data[-2]["time"]])
                print("enter sell m5 close with sl at", sl)
        elif Other.timecheck("forward") < 3:
            data = Other.fetchjson("his")
            result = data[-1]["time"]
            if len(orderlist) == 0:
                orderlist.append(["sell m30 close", asks, sl, takeprofit("sell", cur["mid"]["c"]), prelow])
                print("enter sell m30 close with sl at", sl)
            elif prelow != orderlist[-1][4]:#prelow not in orderlist[-1]:
                orderlist.append(["sell m30 close", asks, sl, takeprofit("sell", cur["mid"]["c"]), prelow])
                print("enter sell m30 close with sl at", sl)
    return orderlist
