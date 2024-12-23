from Data_structure import *
from time import time
from random import random
import PythonTableConsole as PTC

Database = Data()


number_of_random_values = [10**i for i in range(1,7)] # 8 == 4GB RAM, 9 == 12GB RAM, 10 is not recommended
measurements = [["number of values", "time to create plain", "time to create indexed",
                "time to find equals plain", "time to find equals indexed"]]
values = []
for n in number_of_random_values:
    Database.create("plain"+str(n), ["height", "weight", "age"], False)
    Database.create("index"+str(n), ["height", "weight", "age"], [True, True, True])
    measurements.append([n,0,0,0,0])

    for i in range(n-len(values)):
        values.append([int(140+random()*70), int(50+random()*100), int(random()*100)])


    # create plain
    measurements[-1][1] = -time()
    for value in values:
        Database.insert("plain"+str(n), value)
    measurements[-1][1] += time()

    # create indexed
    measurements[-1][2] = -time()
    for value in values:
        Database.insert("index"+str(n), value)
    measurements[-1][2] += time()

    # find equal plain
    measurements[-1][3] = -time()
    Database.select("plain"+str(n),False,["height",values[0][0]])
    measurements[-1][3] += time()

    # find equal indexed
    measurements[-1][4] = -time()
    Database.select("index" + str(n), False, ["height", values[0][0]])
    measurements[-1][4] += time()

table = PTC.PythonTableConsole(measurements)
table.transpose()
print(table)