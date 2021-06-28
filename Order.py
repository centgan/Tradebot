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

def watchnew(pair):
    highandlow = Other.fetchjson("important")
    prehigh = highandlow[pair][-1][0]
    prelow = highandlow[pair][-1][1]
    preprehigh = highandlow[pair][-2][0]
    preprelow = highandlow[pair][-2][1]
    prepreprehigh = highandlow[pair][-3][0]
    prepreprelow = highandlow[pair][-3][1]
    highandlowtime = highandlow[pair][-1][2]

    time = datetime.now()
    time = time.strftime("%d-%m-%Y %H:%M:00")
    format = '%d-%m-%Y %H:%M:%S'

    datahis = Other.fetchjson("his")
    orderdata = Other.fetchjson("order")
    cur = datahis[-1]
    pre = datahis[-2]
    curfile = Other.fetchjson("cur")
    bid = float(curfile["prices"][0]["bids"][0]["price"])
    asks = float(curfile["prices"][0]["asks"][0]["price"])
    #["buy", bid, sl, takeprofit("buy", cur["mid"]["c"], pair), pair, prehigh, proper, "open"]
    for order in orderdata[pair]:
        if order[0] == "buy" and order[7] == "open":
            fullstop = float(order[2])
            halfstop = (float(order[1]) - float(order[2])) / 2
            halfstop = float(order[1]) - halfstop
            time1 = str(order[6])
            time1 = time1[:17]
            time1 += "00"
            if str(datetime.strptime(time, format) - datetime.strptime(time1, format)) == "0:30:00":
                if pre["color"] == "red" and int(pre["body"]) > 3:
                    order[7] = "close"
                    order.append(bid)
                    Other.write("order", orderdata)
            elif bid <= halfstop and len(order) == 8:
                print("close half positions because of stop loss", order)
                order.append("half stop")
            elif bid <= fullstop:
                print("hit full stop loss", order)
                order.append(bid)
                order[7] = "close"
                Other.write("order", orderdata)
            elif bid >= order[1] and len(order) == 9:
                order.pop()
                Other.write("order", orderdata)
            elif preprelow != prelow:
                if float(preprelow) > float(prelow):
                    order[7] = "close"
                    order.append(bid)
                    Other.write("order", orderdata)
            elif preprehigh != preprehigh:
                if float(preprehigh) > float(prehigh):
                    order[7] = "close"
                    order.append(bid)
                    Other.write("order", orderdata)
            elif float(prepreprehigh) > float(preprehigh):
                if str(datetime.strptime(time, format) - datetime.strptime(highandlowtime, format)) == "0:30:00":
                    if datahis[-2]["color"] == "red":
                        order[7] = "close"
                        order.append(asks)
                        Other.write("order", orderdata)

        elif order[0] == "sell" and order[7] == "open":
            fullstop = float(order[2])
            halfstop = (float(order[2]) - float(order[1])) / 2
            halfstop = float(order[1]) + halfstop
            time1 = str(order[6])
            time1 = time1[:17]
            time1 += "00"
            if str(datetime.strptime(time, format) - datetime.strptime(time1, format)) == "0:30:00":
                if pre["color"] == "green" and int(pre["body"]) > 4:
                    order[7] = "close"
                    order.append(asks)
                    Other.write("order", orderdata)
            elif asks >= halfstop and len(order) == 8:
                print("close half positions because of stop loss", order)
                order.append("half stop")
            elif asks >= fullstop:
                print("hit full stop loss", order)
                order.append(asks)
                order[7] = "close"
                Other.write("order", orderdata)
            elif asks <= order[1] and len(order) == 9:
                order.pop()
                Other.write("order", orderdata)
            elif preprelow != prelow:
                if float(preprelow) < float(prelow):
                    order[7] = "close"
                    order.append(asks)
                    Other.write("order", orderdata)
            elif float(prepreprelow) > float(preprelow):
                if str(datetime.strptime(time, format) - datetime.strptime(highandlowtime, format)) == "0:30:00":
                    if datahis[-2]["color"] == "green":
                        order[7] = "close"
                        order.append(asks)
                        Other.write("order", orderdata)
            elif preprehigh != preprehigh:
                if float(preprehigh) < float(prehigh):
                    order[7] = "close"
                    order.append(asks)
                    Other.write("order", orderdata)

def wipe():
    orderdata = Other.fetchjson("order")
    for i in orderdata:
        somelist = [j for j in orderdata[i] if "close" not in j]
        orderdata[i] = somelist
    Other.write("order", orderdata)

def buyorsellnew(pair):
    highandlow = Other.fetchjson("important")

    time = datetime.now()
    proper = time.strftime("%d-%m-%Y %H:%M:%S")

    datahis = Other.fetchjson("his")

    orderdata = Other.fetchjson("order")
    cur = datahis[-1]
    curfile = Other.fetchjson("cur")
    bid = float(curfile["prices"][0]["bids"][0]["price"])
    asks = float(curfile["prices"][0]["asks"][0]["price"])
    prehigh = highandlow[pair][-1][0]
    prelow = highandlow[pair][-1][1]

    if Other.timecheck("hour") == 60 or Other.timecheck("hour") == 30:
        if datahis[-2]["mid"]["c"] > prehigh:
            sl = stoploss("buy")
            if len(orderdata[pair]) == 0:
                orderdata[pair].append(
                    ["buy", bid, sl, takeprofit("buy", cur["mid"]["c"], pair), pair, prehigh, proper, "open"])
                print("enter buy at", bid, sl, pair)
                Other.write("order", orderdata)
            else:
                if len(orderdata[pair]) == 1 and orderdata[pair][-1][1] != "buy":
                    orderdata[pair].append(
                        ["buy", bid, sl, takeprofit("buy", cur["mid"]["c"], pair), pair, prehigh, proper, "open"])
                    print("enter buy at", bid, sl, pair)
                    Other.write("order", orderdata)
                elif len(orderdata[pair]) >= 2:
                    if orderdata[pair][-1][1] != "buy" and orderdata[pair][-2][1] != "buy":
                        orderdata[pair].append(
                            ["buy", bid, sl, takeprofit("buy", cur["mid"]["c"], pair), pair, prehigh, proper, "open"])
                        print("enter buy at", bid, sl, pair)
                        Other.write("order", orderdata)
        elif datahis[-2]["mid"]["c"] < prelow:
            sl = stoploss("sell")
            if len(orderdata[pair]) == 0:
                orderdata[pair].append(
                    ["sell", asks, sl, takeprofit("sell", cur["mid"]["c"], pair), pair, prelow, proper, "open"])
                print("enter sell at", asks, sl, pair)
                Other.write("order", orderdata)
            else:
                if len(orderdata[pair]) == 1 and orderdata[pair][-1][1] != "sell":
                    orderdata[pair].append(
                        ["sell", asks, sl, takeprofit("sell", cur["mid"]["c"], pair), pair, prelow, proper, "open"])
                    print("enter sell at", asks, sl, pair)
                    Other.write("order", orderdata)
                elif len(orderdata[pair]) >= 2:
                    if orderdata[pair][-1][1] != "sell" and orderdata[pair][-2][1] != "sell":
                        orderdata[pair].append(
                            ["sell", asks, sl, takeprofit("sell", cur["mid"]["c"], pair), pair, prelow, proper, "open"])
                        print("enter sell at", asks, sl, pair)
                        Other.write("order", orderdata)
