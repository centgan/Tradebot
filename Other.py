import json
import datetime
from datetime import datetime, timedelta

def propertimestart():
    #for later go by date as in if we ran this program on friday we need to get
    #data from monday so at all times well have 1 full weeks of data excluding weekends
    #so in other words 5 days of data at all times
    weekdays = ["monday", "tuesday"]
    #######change the added time whenever time changes########
    timezone = datetime.now() + timedelta(hours = 4)
    hours = int(timezone.strftime("%H"))
    day = datetime.today().weekday()
    subtract = 0
    if day == 5:
        subtract = 120 + hours
    else:
        subtract = 168
    timesubtract = timezone - timedelta(hours = subtract)
    proper = timesubtract.strftime("%Y-%m-%dT%H:00:00Z")
    return proper

def timestart():
    # with open("numcandles.json", "r") as readfile:
    #     data = json.load(readfile)
    num = 7200
    start = datetime.now() - timedelta(hours=0, minutes=num)
    dt_string = start.strftime("%Y-%m-%dT%H:%M:" + "00Z")
    print(dt_string)
    return dt_string

def fetchjson(doc):
    if doc == "cur":
        with open("cur.json", "r") as read:
            data = json.load(read)
            return data
    elif doc == "his":
        with open("Historicaldata.json", "r") as read:
            data = json.load(read)
            return data
    elif doc == "lower":
        with open("lowertime.json", "r") as read:
            data = json.load(read)
            return data
    elif doc == "important":
        with open("importantinfo.json", "r") as read:
            data = json.load(read)
            return data

def timecheck(forback):
    time = datetime.now()
    new = time + (datetime.min - time) % timedelta(minutes = 30)
    final = str(new - time).lstrip("0:")
    almost = final[:len(final) - 10]
    if forback == "forward":
        return 13
        #return int(almost) + 1
    elif forback == "back":
        return 30 - (int(almost) + 1)
    elif forback == "start":
        rounded = time - (time - datetime.min) % timedelta(minutes=30)
        return rounded.strftime("%Y-%m-%dT%H:%M:00Z")
    
def converter(convertingto, amount, pair):
    pip = {
        "GBP_AUD": 0.0001,
        "NAS100_USD": 1
    }
    amount = float(amount)
    if convertingto == "pip":
        base = pip[pair]
        return float(amount / base)
    elif convertingto == "price":
        base = pip[pair]
        return float(amount * base)
