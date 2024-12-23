from Data_structure import *
from time import time, sleep
from random import random
import PythonTableConsole as PTC
import tqdm
import sys

sys.setrecursionlimit(10**6)

Database = Data()
ERROR = False
time_c = 10**3

def parse_time(time_in):
    if time_in < 10**(-9):
        return "instant"
    if time_in < 10**(-6):
        return str(int(time_in*10**12)/10**3)+"ns"
    if time_in < 10 ** (-3):
        return str(int(time_in * 10 ** 9) / 10 ** 3) + "us"
    if time_in < 1:
        return str(int(time_in * 10 ** 6) / 10 ** 3) + "ms"
    if time_in < 60:
        return str(int(time_in * 10 ** 3) / 10 ** 3) + "s"
    else:
        return str(int(time_in)) + "s"


number_of_random_values = [2**i for i in range(1,17)]
measurements = [["number of values", "time to insert into plain", "time to insert into indexed",
                "= plain", "= indexed", "> plain", "> indexed"]]
values = []
all_values = []
Database.create("plain", ["height", "weight", "age"], False)
Database.create("index", ["height", "weight", "age"], [True, True, True])
for n in number_of_random_values:
    sleep(0.1)
    print("Iteration "+str(n))

    measurements.append([n,0,0,0,0,0,0])
    old_values = values

    values = []
    for i in tqdm.tqdm(range(n-len(old_values)),desc="Generating new values"):
        values.append([int(random()*n - n/2), int(random()*n- n/2), int(random()*n- n/2)])
    all_values += values

    sleep(0.1)
    # insert plain
    measurements[-1][1] = -time()*time_c
    for value in tqdm.tqdm(values, desc="Inserting plain " + str(n)):
        temp = Database.insert("plain", value)
        if isinstance(temp,int):
            if temp<0:
                print(temp)
                print(value)
                exit()
    measurements[-1][1] += time()*time_c
    if len(measurements) > 3:
        measurements[-1][1] += measurements[-2][1]

    sleep(0.1)
    # insert indexed
    measurements[-1][2] = -time()*time_c
    for value in tqdm.tqdm(values,desc="Inserting indexed " + str(n)):
        temp = Database.insert("index", value)
        if isinstance(temp, int):
            if temp < 0:

                print(temp)
                print(value)
                exit()
    measurements[-1][2] += time()*time_c
    if len(measurements) > 3:
        measurements[-1][2] += measurements[-2][2]

    sleep(0.1)
    # find equal indexed
    measurements[-1][4] = -time()*time_c
    for i in tqdm.tqdm(range(n), desc="Finding equal indexed " + str(n)):
        temp = Database.select("index", False, ["height", all_values[i][0], "="])
        if isinstance(temp, int):
            if temp < 0:
                print(temp)
                exit()
    measurements[-1][4] += time()*time_c

    sleep(0.1)
    # find equal plain
    measurements[-1][3] = -time()*time_c
    for i in tqdm.tqdm(range(n),desc = "Finding equal plain " + str(n)):
        temp = Database.select("plain",False,["height",all_values[i][0], "="])
        if isinstance(temp, int):
            if temp < 0:
                print(temp)
                exit()
    measurements[-1][3] += time()*time_c

    sleep(0.1)
    # find greater indexed
    measurements[-1][6] = -time()*time_c
    for i in tqdm.tqdm(range(n), desc="Finding greater indexed " + str(n)):
        temp = Database.select("index", False, ["height", all_values[i][0], ">"])
        if isinstance(temp, int):
            if temp < 0:
                print(temp)
                exit()
    measurements[-1][6] += time()*time_c

    sleep(0.1)
    # find greater plain
    measurements[-1][5] = -time()*time_c
    for i in tqdm.tqdm(range(n), desc="Finding greater plain " + str(n)):
        temp = Database.select("plain", False, ["height", all_values[i][0], ">"])
        if isinstance(temp, int):
            if temp < 0:
                print(temp)
                exit()
    measurements[-1][5] += time()*time_c

    table_map = copy.deepcopy(measurements)
    table_map = [table_map[0]]+[[j[0]] + [parse_time(i) for i in j[1:]] for j in table_map[1:]]
    table = PTC.PythonTableConsole(table_map)
    table.transpose()
    print(table)

input("Press enter to exit")