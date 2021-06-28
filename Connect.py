import mysql.connector
import Other

db = mysql.connector.connect(host = "localhost", user = "test", password = "test123"
                             , database = "test")
cursor = db.cursor()
orderdata = Other.fetchjson("order")

curfile = Other.fetchjson("cur")
bid = curfile["prices"][0]["bids"][0]["price"]
asks = curfile["prices"][0]["asks"][0]["price"]

def checkdb():
    for i in orderdata:
        for j in orderdata[i]:
            entry = j[1]
            com = "SELECT * FROM Orders WHERE Pair = '" + i + "' and Entry = '" + entry + "';"
            cursor.execute(com)
            result = str(cursor.fetchone())
            print(result)
            if result == "None":
                position = j[0]
                entry = j[1]
                stop = j[2]
                tp = j[3]
                pair = j[4]
                time = j[6]
                state = j[7]
                #This will have to be chanaged when going to the actual db
                com = "INSERT INTO Orders (id, entry, close, stop, pair, State)" \
                      "VALUS "

def changes():
    for i in orderdata:
        for j in orderdata[i]:
            entry = j[1]
            com = "SELECT State, Position FROM Orders WHERE Pair = '" + i + "' and Entry = '" + entry + "';"
            cursor.execute(com)
            result = list(cursor.fetchone())
            # result = result.strip('\()')
            # result = result.rstrip('\,')
            # result = result.strip('\'')
            # result = result.strip('\[]')
            if result[0] == "close":
                #this has to change
                j[7] = "close"
                if result[1] == "buy":
                    j.append(bid)
                elif result[1] == "sell":
                    j.append(asks)
                Other.write("order", orderdata)
