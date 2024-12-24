from Data_structure import *
from time import time, sleep
from random import random
import PythonTableConsole as PTC
import tqdm
import sys
import Parser

sys.setrecursionlimit(10**6)

Data = Data()
ERROR = False

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


number_of_random_values = [2**i for i in range(1,11)]
measurements = [["number of values", "time to insert into plain", "time to insert into indexed",
                "= plain", "= indexed", "> plain", "> indexed"]]
values = []
all_values = []
Data.create("plain", ["height", "weight", "age"], False)
Data.create("index", ["height", "weight", "age"], [True, True, True])
for n in number_of_random_values:
    sleep(0.1)
    print("Iteration "+str(n))

    measurements.append([n,0,0,0,0,0,0])
    old_values = values

    values = []
    for i in tqdm.tqdm(range(n-len(old_values)),desc="Generating new values"):
        values.append([int(random()*n - n/2), int(random()*n- n/2), int(random()*100)])
    all_values += values

    sleep(0.1)
    # insert plain
    measurements[-1][1] = -time()
    for value in tqdm.tqdm(values, desc="Inserting plain " + str(n)):
        temp = Data.insert("plain", value)
        if isinstance(temp,int):
            if temp<0:
                print(temp)
                print(value)
                exit()
    measurements[-1][1] += time()
    if len(measurements) > 3:
        measurements[-1][1] += measurements[-2][1]

    sleep(0.1)
    # insert indexed
    measurements[-1][2] = -time()
    for value in tqdm.tqdm(values,desc="Inserting indexed " + str(n)):
        temp = Data.insert("index", value)
        if isinstance(temp, int):
            if temp < 0:

                print(temp)
                print(value)
                exit()
    measurements[-1][2] += time()
    if len(measurements) > 3:
        measurements[-1][2] += measurements[-2][2]

    sleep(0.1)
    # find equal indexed
    measurements[-1][4] = -time()
    for i in tqdm.tqdm(range(n), desc="Finding equal indexed " + str(n)):
        temp = Data.select("index", False, ["height", all_values[i][0], "="])
        if isinstance(temp, int):
            if temp < 0:
                print(temp)
                exit()
    measurements[-1][4] += time()

    sleep(0.1)
    # find equal plain
    measurements[-1][3] = -time()
    for i in tqdm.tqdm(range(n),desc = "Finding equal plain " + str(n)):
        temp = Data.select("plain",False,["height",all_values[i][0], "="])
        if isinstance(temp, int):
            if temp < 0:
                print(temp)
                exit()
    measurements[-1][3] += time()

    sleep(0.1)
    # find greater indexed
    measurements[-1][6] = -time()
    for i in tqdm.tqdm(range(n), desc="Finding greater indexed " + str(n)):
        temp = Data.select("index", False, ["height", all_values[i][0], ">"])
        if isinstance(temp, int):
            if temp < 0:
                print(temp)
                exit()
    measurements[-1][6] += time()

    sleep(0.1)
    # find greater plain
    measurements[-1][5] = -time()
    for i in tqdm.tqdm(range(n), desc="Finding greater plain " + str(n)):
        temp = Data.select("plain", False, ["height", all_values[i][0], ">"])
        if isinstance(temp, int):
            if temp < 0:
                print(temp)
                exit()
    measurements[-1][5] += time()

    table_map = copy.deepcopy(measurements)
    table_map = [table_map[0]]+[[j[0]] + [parse_time(i) for i in j[1:]] for j in table_map[1:]]
    table = PTC.PythonTableConsole(table_map)
    table.transpose()
    print(table)

if __name__ == "__main__":
    while True:
        try:
            string = Parser.recive_input()

        except:
            print("RECEIVE INPUT ERROR. Or end of input, I can't really tell")
            exit()
        if "EXIT" in string.upper() and len(string) < 7:
            break
        if "HELP" in string.upper() and len(string) < 7:
            print(">>>List of all commands:")
            print(">EXIT -- terminates the program. Not syntax sensitive.")
            print(">HELP -- lists all avaliable commands. Not syntax sensitive.")
            print(">CREATE -- creates new table if namaspace is empty. Syntax sensitive: CREATE table_name (column_name [, ...]);")
            print(">INSERT -- inserts row into existing table. Syntax sensitive: INSERT [INTO] table_name (N [, ...]);")
            continue
        prepared_input = Parser.prepare_input(string)
        print(">>>Perceived input: " + prepared_input)
        parsing_result = Parser.parse(prepared_input, Parser.commands)
        # print(parsing_result)

        if isinstance(parsing_result, list):
            if isinstance(parsing_result[1], list):
                match parsing_result[0]:
                    case "CREATE":
                        execution_result = Data.create(parsing_result[1][0],parsing_result[1][1], parsing_result[1][2])
                        match execution_result:
                            case 0:
                                print(">>>Table was created successfully.")
                            case -2:
                                print(">>>EXECUTION ERROR: CREATE. Table already exists.")
                            case -3:
                                print(">>>EXECUTION ERROR: CREATE. Number of column names and number of values in indexing list must match")
                            case _:
                                print(">>>EXECUTION ERROR: CREATE. Cant handle execution result", execution_result)
                    case "INSERT":
                        execution_result = Data.insert(parsing_result[1][0], parsing_result[1][1])
                        match execution_result:
                            case 0:
                                print(">>>Insertion was successful.")
                            case -2:
                                print(">>>EXECUTION ERROR: INSERT. Specified table does not exist")
                                print(">>>Existing tables:")
                                print(Data)
                            case -3:
                                print(">>>EXECUTION ERROR: INSERT. Invalid number of values")
                            case _:
                                print(">>>EXECUTION ERROR: INSERT. Cant handle execution result", execution_result)
                    case "SELECT":
                        execution_result = Data.select(parsing_result[1][0],parsing_result[1][1],parsing_result[1][2],parsing_result[1][3])
                        match execution_result:
                            case -2:
                                print(">>>EXECUTION ERROR: SELECT. Specified table does not exist.")
                                print(">>>Existing tables:")
                                print(Data)
                            case -3:
                                print(">>>EXECUTION ERROR: SELECT. No such column.")
                            case -4:
                                print(">>>EXECUTION ERROR: SELECT. No such aggregating function.")
                            case _:
                                table = PTC.PythonTableConsole([execution_result[0]]+execution_result[1])
                                table.transpose()
                                print(table)
            else:
                match parsing_result[0]:
                    case "CREATE":
                        match parsing_result[1]:
                            case -2:
                                print(">>>INVALID INPUT. Not enough spaces encountered. Must be at least two spaces in CREATE.")
                            case -3.1:
                                print(">>>INVALID INPUT. No opening bracket found.")
                            case -3.2:
                                print(">>>INVALID INPUT. No closing bracket found.")
                            case -4:
                                print(">>>INVALID INPUT. Wrong comma placement")
                            case -5:
                                print(">>>INVALID INPUT. Invalid character.")
                            case _:
                                print(">>>PARSING ERROR: CREATE. Cant handle parsing result", parsing_result)
                    case "INSERT":
                        match parsing_result[1]:
                            case - 2:
                                print(">>>INVALID INPUT. Not enough spaces encountered. Must be at least two spaces in INSERT.")
                            case -3.1:
                                print(">>>INVALID INPUT. No opening bracket found.")
                            case -3.2:
                                print(">>>INVALID INPUT. No closing bracket found.")
                            case -4:
                                print(">>>INVALID INPUT. Wrong comma placement")
                            case -5:
                                print(">>>INVALID INPUT. Invalid character.")
                            case -6:
                                print(">>>INVALID INPUT. Parsing cycle finished wrong. Brackets were never closed.")
                            case -7:
                                print("INVALID INPUT. No digits after minus found")
                            case _:
                                print(">>>PARSING ERROR: INSERT. Cant handle parsing result", parsing_result)
                    case "SELECT":
                        match parsing_result[1]:
                            case -2:
                                print(">>>INVALID INPUT. Not enough spaces encountered. Must be at least two spaces in SELECT.")
                            case -3.1:
                                print(">>>INVALID INPUT. Invalid brackets or spaces structure.")
                            case -3.3:
                                print(">>>INVALID INPUT. Closing bracket was encountered too soon.")
                            case -5:
                                print(">>>INVALID INPUT. Wrong comma placement.")
                            case -6:
                                print(">>>INVALID INPUT. Must not have aggregation if GROUP_BY is not present.")
                            case -7:
                                print(">>>INVALID INPUT. Wrong placement of =, < or >")
                            case _:
                                print(">>>PARSING ERROR: SELECT. Cant handle parsing result", parsing_result)

        else:
            match parsing_result:
                case -3:
                    print(">>>INVALID INPUT. No spaces encountered. Must be at least one space.")
                case -2:
                    print(">>>FAILED TO PARSE. No such command.")
                case _:
                    print(">>>PARSING ERROR. Cant handle parsing result", parsing_result)
    print("end")