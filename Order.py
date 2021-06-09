import Trend
import Other
from datetime import datetime
fullstop = None


# The information here is for current price
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


def watch(revenue, pair):
    datahis = Other.fetchjson("his")
    orderdata = Other.fetchjson("order")
    cur = datahis[-1]
    curfile = Other.fetchjson("cur")
    bid = float(curfile["prices"][0]["bids"][0]["price"])
    asks = float(curfile["prices"][0]["asks"][0]["price"])
    # for values in orderdata.values():
    #     if len(values) == 0:
    #         print(values)
    #     for order in values:
    #         print(order)
    for order in orderdata[pair]:
        if len(order) > 0:
            if order[0] == "buy":
                if len(order) == 9 and order[8] == "move":
                    fullstop = float(order[1])
                else:
                    fullstop = float(order[2])
                halfstopprep = (float(order[1]) - float(order[2])) / 2
                halfstop = float(order[1]) - halfstopprep
                sixer = float(order[1]) + Other.converter("price", 6, pair)
                tener = float(order[1]) + Other.converter("price", 10, pair)
                if bid <= halfstop and len(order) == 8:
                    print("close half positions because of stop loss", order)
                    order.append("half stop")
                    piphalf = Other.converter("pip", halfstopprep, pair)
                    return revenue - piphalf
                elif bid <= fullstop:
                    print("hit full stop loss", order)
                    #full = Other.converter("pip", float(i[2]), pair)
                    piphalf = Other.converter("pip", halfstopprep, pair)
                    order[7] = "close"
                    if len(order) == 10:
                        upprep = float(order[2]) - float(order[1])
                        up = Other.converter("pip", upprep, pair)
                        return revenue + up
                    else:
                        return revenue - piphalf
                elif bid > sixer and len(order) == 8:
                    print("move stop loss to BE")
                    order.append("move")
                    return revenue
                # elif bid >= float(order[3]):
                #     print("take profit full profits", order)
                #     full = Other.converter("pip", float(order[3]), pair)
                #     order[7] = "close"
                #     return revenue + (full - 10)
                elif cur["complete"] == "true" and cur["color"] == "red" and datahis[-2]["color"] == "red":
                    print("closed in prediction of a reversal")
                    order[7] = "close"
                    retval = bid - order[1]
                    retval = Other.converter("pip", retval, pair)
                    return revenue + retval
                elif len(order) == 9:
                    if bid > order[1] and order[8] == "half stop":
                        print("add back to the position")
                        order.pop()
                    elif bid > tener and order[8] == "move":
                        print("close half position for profit")
                        order.append("profit 10")
                        return revenue + 10
                elif len(order) == 10:
                    if bid > (tener + Other.converter("price", 5, pair)):
                        if datahis[-1]["color"] == "green" and Other.timecheck("forward") < 5:
                            if datahis[-1]["Bottom wick"] < datahis[-1]["body"]:
                                order[2] = float(datahis[-1]["mid"]["l"])
                                return revenue
            elif order[0] == "sell":
                if len(order) == 9 and order[8] == "move":
                    fullstop = float(order[1])
                else:
                    fullstop = float(order[2])
                halfstopprep = (float(order[2]) - float(order[1])) / 2
                halfstop = float(order[1]) + halfstopprep
                sixer = float(order[1]) - Other.converter("price", 6, pair)
                tener = float(order[1]) - Other.converter("price", 10, pair)
                if asks >= halfstop and len(order) == 8:
                    print("close half positions because of stop loss", order)
                    order.append("half stop")
                    piphalf = Other.converter("pip", halfstopprep, pair)
                    return revenue - piphalf
                elif asks >= fullstop:
                    print("hit full stop loss", order)
                    piphalf = Other.converter("pip", halfstopprep, pair)
                    order[7] = "close"
                    if len(order) == 10:
                        upprep = float(order[1]) - float(order[2])
                        up = Other.converter("pip", upprep, pair)
                        return revenue + up
                    else:
                        return revenue - piphalf
                elif asks < sixer and len(order) == 8:
                    print("move stop loss to BE")
                    order.append("move")
                    return revenue
                # elif asks <= float(order[3]):
                #     print("take profit full profits", order)
                #     full = Other.converter("pip", float(order[3]), pair)
                #     order[7] = "close"
                #     return revenue + (full - 10)
                elif cur["complete"] == "true" and cur["color"] == "green" and datahis[-2]["color"] == "green":
                    print("closed in prediction of a reversal")
                    order[7] = "close"
                    retval = order[1] - asks
                    retval = Other.converter("pip", retval, pair)
                    return revenue + retval
                elif len(order) == 9:
                    if asks < order[1] and order[8] == "half stop":
                        print("add back to the position")
                        order.pop()
                    elif bid < tener and order[8] == "move":
                        print("close half position for profit")
                        order.append("profit 10")
                        return revenue + 10
                elif len(order) == 10:
                    if asks < (tener - Other.converter("price", 5, pair)):
                        if datahis[-1]["color"] == "red" and Other.timecheck("forward") < 5:
                            if datahis[-1]["Top wick"] < datahis[-1]["body"]:
                                order[2] = float(datahis[-1]["mid"]["h"])
                                return revenue
    return revenue 

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

    orderdata = Other.fetchjson("order")

    if float(cur["mid"]["c"]) > float(prehigh):
        #other.timecheck("forward") results in the time remaining NOT the time it has taken
        sl = stoploss("buy")
        if Other.timecheck("forward") == 15:
            Trend.lower("M15", pair)
            data = Other.fetchjson("lower")
            if len(orderdata[pair]) == 0 and data[-2]["mid"]["c"] > prehigh:
                orderdata[pair].append(["buy", bid, sl, takeprofit("buy", cur["mid"]["c"], pair), pair, prehigh, proper, "open"])
                print("enter buy m15 close with sl at", sl)
                Other.write("order", orderdata)
                return
            else:
                if orderdata[pair][-1][1] != "buy":
                    if len(orderdata[pair]) == 1 and data[-2]["mid"]["c"] > prehigh:
                        orderdata[pair].append(["buy", bid, sl, takeprofit("buy", cur["mid"]["c"], pair), pair, prehigh, proper, "open"])
                        print("enter buy m15 close with sl at", sl)
                        Other.write("order", orderdata)
                        return
                    elif len(orderdata[pair]) >= 2 and orderdata[pair][-2][1] != "buy" and data[-2]["mid"]["c"] > prehigh:
                        orderdata[pair].append(["buy", bid, sl, takeprofit("buy", cur["mid"]["c"], pair), pair, prehigh, proper, "open"])
                        print("enter buy m15 close with sl at", sl)
                        Other.write("order", orderdata)
                        return

        elif Other.timecheck("forward") == 30:
            if len(orderdata[pair]) == 0 and datahis[-2]["mid"]["c"] > prehigh:
                orderdata[pair].append(["buy", bid, sl, takeprofit("buy", cur["mid"]["c"], pair), pair, prehigh, proper, "open"])
                print("enter buy m30 close with sl at", sl)
                Other.write("order", orderdata)
                return
            else:
                if orderdata[pair][-1][1] != "buy":
                    if len(orderdata[pair]) == 1 and datahis[-2]["mid"]["c"] > prehigh:
                        orderdata[pair].append(
                            ["buy", bid, sl, takeprofit("buy", cur["mid"]["c"], pair), pair, prehigh, proper, "open"])
                        print("enter buy m30 close with sl at", sl)
                        Other.write("order", orderdata)
                        return
                    elif len(orderdata[pair]) >= 2 and orderdata[pair][-2][1] != "buy" and datahis[-2]["mid"]["c"] > prehigh:
                        orderdata[pair].append(
                            ["buy", bid, sl, takeprofit("buy", cur["mid"]["c"], pair), pair, prehigh, proper, "open"])
                        print("enter buy m30 close with sl at", sl)
                        Other.write("order", orderdata)
                        return

    elif float(cur["mid"]["c"]) < float(prelow):
        sl = stoploss("sell")
        if Other.timecheck("forward") == 15:
            Trend.lower("M15", pair)
            data = Other.fetchjson("lower")
            if len(orderdata[pair]) == 0 and data[-2]["mid"]["c"] < prelow:
                orderdata[pair].append(["sell", asks, sl, takeprofit("sell", cur["mid"]["c"], pair), pair, prelow, proper, "open"])
                print("enter sell m15 close with sl at", sl)
                Other.write("order", orderdata)
                return
            else:
                if orderdata[pair][-1][1] != "sell":
                    if len(orderdata[pair]) == 1 and data[-2]["mid"]["c"] < prelow:
                        orderdata[pair].append(["sell", asks, sl, takeprofit("sell", cur["mid"]["c"], pair), pair, prelow, proper, "open"])
                        print("enter sell m15 close with sl at", sl)
                        Other.write("order", orderdata)
                        return
                    elif len(orderdata[pair]) >= 2 and orderdata[pair][-2][1] != "sell" and data[-2]["mid"]["c"] < prelow:
                        orderdata[pair].append(["sell", asks, sl, takeprofit("sell", cur["mid"]["c"], pair), pair, prelow, proper, "open"])
                        print("enter sell m15 close with sl at", sl)
                        Other.write("order", orderdata)
                        return

        elif Other.timecheck("forward") == 30:
            if len(orderdata[pair]) == 0 and datahis[-2]["mid"]["c"] < prelow:
                orderdata[pair].append(["sell", asks, sl, takeprofit("sell", cur["mid"]["c"], pair), pair, prelow, proper, "open"])
                print("enter sell m30 close with sl at", sl)
                Other.write("order", orderdata)
                return
            else:
                if orderdata[pair][-1][1] != "sell":
                    if len(orderdata[pair]) == 1 and datahis[-2]["mid"]["c"] < prelow:
                        orderdata[pair].append(["sell", asks, sl, takeprofit("sell", cur["mid"]["c"], pair), pair, prelow, proper, "open"])
                        print("enter sell m30 close with sl at", sl)
                        Other.write("order", orderdata)
                        return
                    elif len(orderdata[pair]) >= 2 and orderdata[pair][-2][1] != "sell" and datahis[-2]["mid"]["c"] < prelow:
                        orderdata[pair].append(["sell", asks, sl, takeprofit("sell", cur["mid"]["c"], pair), pair, prelow, proper, "open"])
                        print("enter sell m30 close with sl at", sl)
                        Other.write("order", orderdata)
                        return
