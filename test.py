from Data_structure import *
from time import time, sleep
from random import random
import PythonTableConsole as PTC
import tqdm

Database = Data()
ERROR = False


number_of_random_values = [2**i for i in range(1,15)]
measurements = [["number of values", "time to insert into plain", "time to insert into indexed",
                "= plain", "= indexed", "> plain", "> indexed"]]
values = []
for n in number_of_random_values:
    sleep(0.1)
    print("Iteration "+str(n))
    Database.create("plain"+str(n), ["height", "weight", "age"], False)
    Database.create("index"+str(n), ["height", "weight", "age"], [True, True, True])
    measurements.append([n,0,0,0,0,0,0])

    for i in tqdm.tqdm(range(n-len(values)),desc="Generating new values"):
        values.append([int(random()*n - n/2), int(random()*n- n/2), int(random()*n- n/2)])

    sleep(0.1)
    # insert plain
    measurements[-1][1] = -time()
    for value in tqdm.tqdm(values, desc="Inserting plain " + str(n)):
        temp = Database.insert("plain"+str(n), value)
        if isinstance(temp,int):
            if temp<0:
                print(temp)
                print(value)
                exit()
    measurements[-1][1] += time()

    sleep(0.1)
    # insert indexed
    measurements[-1][2] = -time()
    for value in tqdm.tqdm(values,desc="Inserting indexed " + str(n)):
        temp = Database.insert("index" + str(n), value)
        if isinstance(temp, int):
            if temp < 0:

                print(temp)
                print(value)
                exit()
    measurements[-1][2] += time()

    sleep(0.1)
    # find equal indexed
    measurements[-1][4] = -time()
    for i in tqdm.tqdm(range(n), desc="Finding equal indexed " + str(n)):
        temp = Database.select("index" + str(n), False, ["height", values[i][0], "="])
        if isinstance(temp, int):
            if temp < 0:
                print(temp)
                exit()
    measurements[-1][4] += time()

    sleep(0.1)
    # find equal plain
    measurements[-1][3] = -time()
    for i in tqdm.tqdm(range(n),desc = "Finding equal plain " + str(n)):
        temp = Database.select("plain"+str(n),False,["height",values[i][0], "="])
        if isinstance(temp, int):
            if temp < 0:
                print(temp)
                exit()
    measurements[-1][3] += time()

    sleep(0.1)
    # find greater indexed
    measurements[-1][6] = -time()
    for i in tqdm.tqdm(range(n), desc="Finding greater indexed " + str(n)):
        temp = Database.select("index" + str(n), False, ["height", values[i][0], ">"])
        if isinstance(temp, int):
            if temp < 0:
                print(temp)
                exit()
    measurements[-1][6] += time()

    sleep(0.1)
    # find greater plain
    measurements[-1][5] = -time()
    for i in tqdm.tqdm(range(n), desc="Finding greater plain " + str(n)):
        temp = Database.select("plain" + str(n), False, ["height", values[i][0], ">"])
        if isinstance(temp, int):
            if temp < 0:
                print(temp)
                exit()
    measurements[-1][5] += time()



    table = PTC.PythonTableConsole(measurements)
    table.transpose()
    print(table)

input("Press enter to exit")