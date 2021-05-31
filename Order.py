import Trend
import Other
from datetime import datetime
fullstop = 0

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

def takeprofit(sellorbuy, cur, pair):
    if sellorbuy == "sell":
        converted = Other.converter("price", 25, pair)
        cur = float(cur) - converted
        return cur
    elif sellorbuy == "buy":
        converted = Other.converter("price", 25, pair)
        cur = float(cur) + converted
        return cur

def watch(orderlist, revenue, pair):
    datahis = Other.fetchjson("his")
    cur = datahis[-1]
    curfile = Other.fetchjson("cur")
    bid = float(curfile["prices"][0]["bids"][0]["price"])
    asks = float(curfile["prices"][0]["asks"][0]["price"])
    for i in orderlist:
        if i[7] == "open":
            if "buy" in i[0]:
                if "move" in i[8]:
                    fullstop = float(i[1])
                else:
                    fullstop = float(i[2])
                halfstopprep = (float(i[1]) - float(i[2])) / 2
                halfstop = float(i[1]) - halfstopprep
                sixer = float(i[1]) + Other.converter("price", 6, pair)
                tener = float(i[1]) + Other.converter("price", 10, pair)
                if bid <= halfstop and len(i) == 7:
                    print("close half positions because of stop loss", i)
                    i.append("half stop")
                    piphalf = Other.converter("pip", halfstopprep, pair)
                    return revenue - piphalf
                elif bid <= fullstop:
                    print("hit full stop loss", i)
                    #full = Other.converter("pip", float(i[2]), pair)
                    piphalf = Other.converter("pip", halfstopprep, pair)
                    i[7] = "close"
                    return revenue - piphalf
                elif bid > sixer and len(i) == 7:
                    print("move stop loss to BE")
                    i.append("move")
                elif bid >= float(i[3]):
                    print("take profit full profits", i)
                    full = Other.converter("pip", float(i[3]), pair)
                    i[7] = "close"
                    return revenue + (full - 10)
                elif cur["complete"] == "true" and cur["color"] == "red" and datahis[-2]["color"] == "red":
                    print("closed in prediction of a reversal")
                    i[7] = "close"
                if len(i) == 8:
                    if bid > i[1] and i[8] == "half stop":
                        print("add back to the position")
                        i.pop()
                    elif bid > tener and i[8] == "move":
                        print("close half position for profit")
                        i.append("profit 10")
                        return revenue + 10
            elif "sell" in i[0]:
                if "move" in i[8]:
                    fullstop = float(i[1])
                else:
                    fullstop = float(i[2])
                halfstopprep = (float(i[2]) - float(i[1])) / 2
                halfstop = float(i[1]) + halfstopprep
                sixer = float(i[1]) - Other.converter("price", 6, pair)
                tener = float(i[1]) - Other.converter("price", 10, pair)
                if asks >= halfstop and len(i) == 7:
                    print("close half positions because of stop loss", i)
                    i.append("half stop")
                    piphalf = Other.converter("pip", halfstopprep, pair)
                    return revenue - piphalf
                elif asks >= float(i[2]):
                    print("hit full stop loss", i)
                    piphalf = Other.converter("pip", halfstopprep, pair)
                    i[7] = "close"
                    return revenue - piphalf
                elif asks < sixer and len(i) == 7:
                    print("move stop loss to BE")
                    i.append("move")
                elif asks <= float(i[3]):
                    print("take profit full profits", i)
                    full = Other.converter("pip", float(i[3]), pair)
                    i[7] = "close"
                    return revenue + (full - 10)
                elif cur["complete"] == "true" and cur["color"] == "green" and datahis[-2]["color"] == "green":
                    print("closed in prediction of a reversal")
                    i[7] = "close"
                if len(i) == 8:
                    if asks < i[1] and i[8] == "half stop":
                        print("add back to the position")
                        i.pop()
                    elif bid < tener and i[8] == "move":
                        print("close half position for profit")
                        i.append("profit 10")
                        return revenue + 10

orderlist = []
def buyorsell(pair):
    result = Trend.overall()
    zone = result[0]
    order = result[1]
    highandlow = result[2]

    time = datetime.now()
    proper = time.strftime("%H:%M:%S")

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
            Trend.lower("M15", pair)
            data = Other.fetchjson("lower")
            if len(orderlist) == 0 and data[-2]["mid"]["c"] > prehigh:
                orderlist.append(["buy m15 close", bid, sl, takeprofit("buy", cur["mid"]["c"], pair), pair, prehigh, proper, "open"])
                print("enter buy  m15 close with sl at", sl)
            elif data[-2]["mid"]["c"] > prehigh and ((prehigh != orderlist[-1][5] and pair == orderlist[-1][4]) or (prehigh != orderlist[-1][5] and pair == orderlist[-1][4])):
                orderlist.append(["buy m15 close", bid, sl, takeprofit("buy", cur["mid"]["c"], pair), pair, prehigh, proper, "open"])
                print("enter buy  m15 close with sl at", sl)
        #5min close will have be modified later
        # elif 3 < Other.timecheck("forward") < 10:
        #     Trend.lower("M5", "GBP_AUD")
        #     data = Other.fetchjson("lower")
        #     if len(orderlist) == 0 and data[-2]["mid"]["c"] > prehigh:
        #         orderlist.append(["buy m5 close", bid, sl, takeprofit("buy", cur["mid"]["c"]), proper])
        #         print("enter buy  m15 close with sl at", sl)
        #     elif data[-2]["mid"]["c"] > prehigh and prehigh != orderlist[-1][4]:#prehigh not in orderlist[-1]:
        #         orderlist.append(["buy m5 close", bid, sl, takeprofit("buy", cur["mid"]["c"]), proper])
        #         print("enter buy m5 close with sl at", sl)
        elif Other.timecheck("forward") == 30:
            if len(orderlist) == 0 and cur["mid"]["c"] > prehigh:
                orderlist.append(["buy m30 close", bid, sl, takeprofit("buy", cur["mid"]["c"], pair), pair, prehigh, proper, "open"])
                print("enter buy m30 close with sl at", sl)
            elif cur["mid"]["c"] > prehigh and ((prehigh != orderlist[-1][5] and pair == orderlist[-1][4]) or (prehigh != orderlist[-1][5] and pair == orderlist[-1][4])):
                orderlist.append(["buy m30 close", bid, sl, takeprofit("buy", cur["mid"]["c"], pair), pair, prehigh, proper, "open"])
                print("enter buy m30 close with sl at", sl)
    elif float(cur["mid"]["c"]) < float(prelow):
        sl = stoploss("sell")
        if 12 < Other.timecheck("forward") <= 15:
            Trend.lower("M15", pair)
            data = Other.fetchjson("lower")
            if len(orderlist) == 0 and data[0]["mid"]["c"] < prelow:
                orderlist.append(["sell m15 close", asks, sl, takeprofit("sell", cur["mid"]["c"], pair), pair, prelow, proper, "open"])
                print("enter sell m15 close with sl at", sl)
            elif data[0]["mid"]["c"] < prelow and ((prelow != orderlist[-1][5] and pair == orderlist[-1][4]) or (prelow != orderlist[-1][5] and pair == orderlist[-1][4])):
                orderlist.append(["sell m15 close", asks, sl, takeprofit("sell", cur["mid"]["c"], pair), pair, prelow, proper, "open"])
                print("enter sell  m15 close with sl at", sl)
        # elif 3 < Other.timecheck("forward") < 8:
        #     Trend.lower("M5", "GBP_AUD")
        #     data = Other.fetchjson("lower")
        #     if len(orderlist) == 0 and data[0]["mid"]["c"] < prelow:
        #         orderlist.append(["sell m5 close", asks, sl, takeprofit("sell", cur["mid"]["c"]), proper])
        #         print("enter sell m5 close with sl at", sl)
        #     elif data[-2]["mid"]["c"] < prelow and prelow != orderlist[-1][4]:#prelow not in orderlist[-1]:
        #         orderlist.append(["sell m5 close", asks, sl, takeprofit("sell", cur["mid"]["c"]), proper])
        #         print("enter sell m5 close with sl at", sl)
        elif Other.timecheck("forward") == 30:
            if len(orderlist) == 0:
                orderlist.append(["sell m30 close", asks, sl, takeprofit("sell", cur["mid"]["c"], pair), pair, prelow, proper, "open"])
                print("enter sell m30 close with sl at", sl)
            elif prelow < orderlist[-1][4] and ((prehigh != orderlist[-1][5] and pair == orderlist[-1][4]) or (prehigh != orderlist[-1][5] and pair == orderlist[-1][4])):
                orderlist.append(["sell m30 close", asks, sl, takeprofit("sell", cur["mid"]["c"], pair), pair, prelow, proper, "open"])
                print("enter sell m30 close with sl at", sl)
    return orderlist
