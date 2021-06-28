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

    if day == 5:
        subtract = 120 + hours
    else:
        subtract = 168
    timesubtract = timezone - timedelta(hours = subtract)
    proper = timesubtract.strftime("%Y-%m-%dT%H:00:00Z")
    return proper

def hourstart():
    check = timecheck("hour")
    check = 60 - check
    time = datetime.now() - timedelta(minutes = check)
    final = time - timedelta(hours = 1)
    format = final.strftime("%Y-%m-%dT%H:00:00Z")
    return format

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
    elif doc == "order":
        with open("Orderlist.json", "r") as read:
            data = json.load(read)
            return data
    elif doc == "half":
        with open("Half.json", "r") as read:
            data = json.load(read)
            return data

def write(file, data):
    if file == "cur":
        with open("cur.json", "w") as out:
            out.write(json.dumps(data, indent=4))
    elif file == "his":
        with open("Historicaldata.json", "w") as out:
            out.write(json.dumps(data, indent=4))
    elif file == "lower":
        with open("lowertime.json", "w") as out:
            out.write(json.dumps(data, indent=4))
    elif file == "important":
        with open("importantinfo.json", "w") as out:
            out.write(json.dumps(data, indent=4))
    elif file == "order":
        with open("Orderlist.json", "w") as out:
            out.write(json.dumps(data, indent=4))
    elif file == "half":
        with open("Half.json", "w") as out:
            out.write(json.dumps(data, indent = 4))

def timecheck(forback):
    time = datetime.now()
    new = time + (datetime.min - time) % timedelta(minutes = 30)
    hourly = time + (datetime.min - time) % timedelta(minutes = 60)
    hourlystrip = str(hourly - time).lstrip("0:")
    almosthour = hourlystrip[:len(hourlystrip) - 10]
    final = str(new - time).lstrip("0:")
    almost = final[:len(final) - 10]
    if forback == "forward":
        return float(almost) + 1
    elif forback == "back":
        return 30 - (float(almost) + 1)
    elif forback == "start":
        rounded = time - (time - datetime.min) % timedelta(minutes=30)
        return rounded.strftime("%Y-%m-%dT%H:%M:00Z")
    elif forback == "hour":
        return float(almosthour) + 1

def converter(convertingto, amount, pair):
    pip = {
        "GBP_AUD": 0.0001,
        "GBP_USD": 0.0001,
        "NAS100_USD": 1
    }
    amount = float(amount)
    if convertingto == "pip":
        base = pip[pair]
        return round(float(amount / base), 1)
    elif convertingto == "price":
        base = pip[pair]
        return round(float(amount * base), 1)
