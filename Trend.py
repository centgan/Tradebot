import json
from oandapyV20 import API
import oandapyV20.endpoints.pricing as pricing
from oandapyV20.contrib.factories import InstrumentsCandlesFactory
import Other
from datetime import datetime

idaccount = ""
token = ""
client = API(access_token = token)
state = ""
changetime = ""
pullbackup = 0
pullbackdown = 0
singlered = 0
highest = 0
lowest = 0

def pattern(closeoropen, pair):
    datahis = Other.fetchjson("his")
    half = Other.fetchjson("half")
    # Possibly also include the proper color candle meaning opposite color
    if closeoropen == "close":
        if 59 <= Other.timecheck("hour") <= 60:
            top = float(datahis[-2]["Top wick"])/float(datahis[-2]["body"])
            bottom = float(datahis[-2]["Bottom wick"])/float(datahis[-2]["body"])
            top = Other.converter("pip", top, pair)
            bottom = Other.converter("pip", bottom, pair)

            if top > 1.5 or bottom > 1.5 and abs(top - bottom) < 2:
                return "close"
    if closeoropen == "open":
        top = half[-3]
        if half[-3]:
            pass


def overall(pair):
    data = Other.fetchjson("his")
    alist = []

    time = datetime.now()
    proper = time.strftime("%d-%m-%Y %H:%M:00")

    # may have to move this section somewhere else to improve maybe even get rid of completely
    # because this is for historical and not current price
    previoushigh = 0
    previouslow = 0
    highandlow = Other.fetchjson("important")
    if Other.timecheck("hour") == 60 or Other.timecheck("hour") == 30:
        if data[-1]["color"] == "green" and data[-2]["color"] == "red":
            previouslow = data[-2]["mid"]["l"]
        elif data[-1]["color"] == "red" and data[-2]["color"] == "green":
            previoushigh = data[-2]["mid"]["h"]
    if previouslow != 0 or previoushigh != 0:
        highandlow[pair].append([previoushigh, previouslow, proper])
        Other.write("important", highandlow)
        print("get")

    # for i in range(len(data)):
    #     j = i + 1
    #     if j == len(data):
    #         break
    #     if data[i]["color"] == "green" and data[j]["color"] == "red":
    #         previoushigh = data[i]["mid"]["h"]
    #     elif data[i]["color"] == "red" and data[j]["color"] == "green":
    #         previouslow = data[i]["mid"]["l"]
    #     highandlow.append([previoushigh, previouslow])
    # this next section could be removed, not really necessary but leave it for now
    for i in range(len(data)):
        j = i + 1
        if j == len(data):
            break
        if "pullback" in data[i]["trend"]:
            alist.append(data[i]["time"])
        if data[i]["trend"] == "pullback uptrend" and data[j]["trend"] != "pullback uptrend":
            data[i]["trend"] = "uptrend"
    with open("Historicaldata.json", "w") as out:
        out.write(json.dumps(data, indent = 4))
    # as of right now orderlist is not needed but leave it as things can change

def trendassign(listnum):
    global state, changetime, pullbackup, pullbackdown, singlered
    # data is a list of dictionaries
    data = Other.fetchjson("his")
    # lists is the list of candles for the uptrend and downtrend
    lists = trendprep()
    returndata = ["trend"]
    # uplist is the first list in lists cause trendprep returns a list of lists
    uplist = lists[0]
    # same thing as uplist but its downtrend now
    downlist = lists[1]
    if data[0]["time"] == listnum["time"]:
        if uplist[0][0] < downlist[0][0]:
            # for uptrend
            changetime = data[uplist[0][0]]["time"]
            state = "uptrend"
        else:
            # for downtrend
            changetime = data[uplist[0][0]]["time"]
            state = "downtrend"
    timeindex = next((index for (index, d) in enumerate(data) if d["time"] == changetime), None)
    if state == "uptrend":
        lowestbeforereversal = data[timeindex]["mid"]["o"]
        if listnum["mid"]["c"] < lowestbeforereversal:
            returndata.append("reversal going down")
            state = "downtrend"
            changetime = listnum["time"]
        # elif listnum["color"] == "green" and pullbackup > 0:
        #     changetime = listnum["time"]
        #     pullbackup = 0
        #     changetime = listnum["time"]
        #     returndata.append("pullback ")
        #     print(listnum["time"], "bunch")
        #     # elif listnum["color"] == "red":
        #     #     returndata.append("pullback")
        #     # changetime = listnum["time"]
        elif listnum["color"] == "red":
            pullbackup += 1
            returndata.append("pullback uptrend")
        else:
            returndata.append("uptrend")
        if listnum["color"] == "green" and pullbackup > 0:
            changetime = listnum["time"]
            pullbackup = 0
    elif state == "downtrend":
        highestbeforreversal = data[timeindex]["mid"]["o"]
        if listnum["mid"]["c"] > highestbeforreversal:
            returndata.append("reversal going up")
            state = "uptrend"
            changetime = listnum["time"]
            # print(changetime)
        # elif listnum["color"] == "red" and pullbackdown > 0 and listnum["mid"]["c"] > highestbeforreversal:
        #     changetime = listnum["time"]
        #     pullbackdown = 0
        #     changetime = listnum["time"]
        #     returndata.append("pullback")
        # elif listnum["color"] == "red":
        #     returndata.append("pullback")
        #     changetime = listnum["time"]
        elif listnum["color"] == "green":
            pullbackdown += 1
            returndata.append("pullback downtrend")
        else:
            returndata.append("downtrend")
        if listnum["color"] == "red" and pullbackdown > 0:
            changetime = listnum["time"]
            pullbackdown = 0
    return returndata

def trendprep():
    data = Other.fetchjson("his")
    downtrendlist = []
    uptrendlist = []
    # if data[0]["color"] == "red":
    #     firstredwick = data[0]["mid"]["l"]
    #     firstredbody = data[0]["mid"]["c"]
    for front in range(len(data)):
        back = front - 1
        if back == -1:
            back = 0
        frontredwick = data[front]["mid"]["l"]
        frontredbody = data[front]["mid"]["c"]
        backredwick = data[back]["mid"]["l"]
        backredbody = data[back]["mid"]["c"]
        frontgreenwick = data[front]["mid"]["l"]
        frontgreenbody = data[front]["mid"]["c"]
        backgreenwick = data[back]["mid"]["l"]
        backgreenbody = data[back]["mid"]["c"]
        if frontredbody < backredbody:
            downtrendlist.append([back, front])
        elif frontgreenbody > backgreenbody:
            uptrendlist.append([back, front])
    # puts all candles that were lower than the previous into a list in pairs
    for i in range(len(downtrendlist)):
        j = i + 1
        if j == len(downtrendlist):
            break
        if int(downtrendlist[i][1]) == int(downtrendlist[j][0]):
            downtrendlist[i].extend(downtrendlist[j])
    for l in range(len(uptrendlist)):
        m = l + 1
        if m == len(uptrendlist):
            break
        if int(uptrendlist[l][1]) == int(uptrendlist[m][0]):
            uptrendlist[l].extend(uptrendlist[m])
    # filters out the single pair candles and common numbers
    downtransfer = []
    uptransfer = []
    for i in downtrendlist:
        if len(i) > 2:
            del i[1], i[1]
            downtransfer.append(i)
    downtrendlist = downtransfer
    for l in uptrendlist:
        if len(l) > 2:
            del l[1], l[1]
            uptransfer.append(l)
    uptrendlist = uptransfer

    return uptrendlist, downtrendlist

def halfdump(instrument):
    start = Other.hourstart()
    param = {
        "from": start,
        "granularity": "M30"
    }
    with open("Half.json".format(instrument, "M30"), "w") as out:
        for i in InstrumentsCandlesFactory(instrument = instrument, params = param):
            client.request(i)
            out.write(json.dumps(i.response.get("candles"), indent = 4))

def dumphist(instrument, gran):
    result = Other.propertimestart()
    param = {
        "from": result,
        "granularity": gran
    }
    # in the future can optimize this by not writing it to the json file so much
    with open("Historicaldata.json".format(instrument, gran), "w") as out:
        for i in InstrumentsCandlesFactory(instrument = instrument, params = param):
            client.request(i)
            out.write(json.dumps(i.response.get("candles"), indent = 4))
    with open("Historicaldata.json".format(instrument, gran), "r") as read:
        data = json.load(read)
        for i in data:
            openprice = float(i["mid"]["o"])
            closeprice = float(i["mid"]["c"])
            final = float(closeprice) - float(openprice)
            if final > 0:
                twgreen = float(i["mid"]["h"]) - closeprice
                bwgreen = float(i["mid"]["l"]) - openprice
                i.__setitem__("color", "green")
                i.__setitem__("body", str(round(final, 5)))
                i.__setitem__("Top wick", str(round(twgreen, 5)))
                i.__setitem__("Bottom wick", str(round(bwgreen, 5)))
            elif final < 0:
                twred = float(i["mid"]["h"]) - openprice
                bwred = float(i["mid"]["l"]) - closeprice
                i.__setitem__("color", "red")
                i.__setitem__("body", str(round(final, 5)))
                i.__setitem__("Top wick", str(round(twred, 5)))
                i.__setitem__("Bottom wick", str(round(bwred, 5)))
            elif final == 0:
                i.__setitem__("color", "equal")
                i.__setitem__("body", str(round(final, 5)))
            result = trendassign(i)
            i.__setitem__(result[0], result[1])
        with open("Historicaldata.json".format(instrument, gran), "w") as out:
            out.write(json.dumps(data, indent = 4))

def dumpcur(instrument):
    params = {"instruments": instrument}
    r = pricing.PricingInfo(accountID = idaccount, params = params)

    with open("cur.json", "w") as out:
        client.request(r)
        out.write(json.dumps(r.response, indent = 4))
# planning on using another method to get this info
def difdumpcur(instrument):
    pass
