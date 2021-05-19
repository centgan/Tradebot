import Other

data = Other.fetchjson("his")
def zonefinding():
    zonelist = []
    zonelistfilterone = []
    counter = 0
    # localhigh = float(0)
    # localmin = float(100)

    #this can be optimized significantly first leave it like this cause it works
    for i in range(len(data)):
        j = i + 1
        if j == len(data):
            break
        if data[i]["color"] != data[j]["color"]:
            if data[i]["color"] == "red":
                zonelist.append(data[i]["mid"]["c"])
            elif data[i]["color"] == "green":
                zonelist.append(data[i]["mid"]["c"])
    for i in zonelist:
        for j in zonelist:
            if (abs(float(i) - float(j)) <= 0.0001) and (float(i) - float(j) != 0):
                # zonelistfilterone.__setitem__("bottom", )
                if float(i) > float(j):
                    zonelistfilterone.append([j, i])
                else:
                    zonelistfilterone.append([i, j])
                counter += 1
    print(zonelistfilterone)
    print(zonelist)
    for i in range(len(zonelistfilterone)):
        for j in range(len(zonelistfilterone)):
            if zonelistfilterone[i][0] == zonelistfilterone[j][0] and zonelistfilterone[i][1] != zonelistfilterone[j][1]:
                print(zonelistfilterone[i], zonelistfilterone[j])
        # j = i + 1
        # if j == len(zonelistfilterone):
        #     break
        # if zonelistfilterone[i][0] == zonelistfilterone[j][0]:
    # for i in range(len(data)):
    #     if counter < 10:
    #         if float(data[i]["mid"]["c"]) > localhigh:
    #             localhigh = float(data[i]["mid"]["c"])
    #         elif float(data[i]["mid"]["c"]) < localmin:
    #             localmin = float(data[i]["mid"]["c"])
    #         #print(localhigh, localmin)
    #         print(counter)
    #         counter += 1
    #     elif counter == 10:
    #         counter = 0
    # for i in range(len(data)):
    #     j = i + 1
    #     if j == len(data):
    #         break
    #     # print(i["color"])
    #     # print(j["color"])
    #     if data[i]["color"] != data[j]["color"]:
    #         if data[i]["color"] == "red":
    #             zonelist.extend([data[i]["mid"]["c"], data[i]["time"]])
    #         elif data[i]["color"] == "green":
    #             zonelist.extend([data[i]["mid"]["c"], data[i]["time"]])
    #         # print(data[i]["time"])
    #         # print(data[j]["time"])
    #         counter += 1
    # print(zonelist)
    # print(counter)