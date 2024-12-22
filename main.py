import Parser
import Data_structure

Data = Data_structure.Data()

while True:
    string = Parser.recive_input()
    if "EXIT" in string.upper() and len(string) < 7:
        break
    if "HELP" in string.upper() and len(string) < 7:
        print(">>>List of all commands:")
        print(">EXIT -- terminates the program. Not syntax sensitive.")
        print(">HELP -- lists all avaliable commands. Not syntax sensitive.")
        print(">CREATE -- creates new table if namaspace is empty. Syntax sensitive: CREATE table_name (column_name [, ...]);")
        print(">INSERT -- inserts row into existing table. Syntax sensitive: INSERT [INTO] table_name (N [, ...]);")
        continue
    parsing_result = Parser.parse(Parser.prepare_input(string), Parser.commands)
    print(parsing_result)
    if isinstance(parsing_result, list):
        if isinstance(parsing_result[1], list):
            match parsing_result[0]:
                case "CREATE":
                    execution_result = Data.create(parsing_result[1][0],parsing_result[1][1])
                    match execution_result:
                        case 0:
                            print(">>>Table was created successfully.")
                        case -2:
                            print(">>>EXECUTION ERROR: CREATE. Table already exists.")
                        case _:
                            print(">>>EXECUTION ERROR: CREATE. Cant handle execution result", execution_result)
                case "INSERT":
                    execution_result = Data.insert(parsing_result[1][0], parsing_result[1][1])
                    match execution_result:
                        case 0:
                            print(">>>Insertion was successful")
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
                            print(">>>EXECUTION ERROR: SELECT. Specified table does not exist")
                            print(">>>Existing tables:")
                            print(Data)
                        case -3:
                            print(">>>EXECUTION ERROR: SELECT. No such column")
                        case -4:
                            print(">>>EXECUTION ERROR: SELECT. No such aggregating function")
                        case _:
                            for row in execution_result:
                                print(row)
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
                            print(">>>INVALID INPUT. Parsing cycle finished wrong. Please check string's quotation marks.")
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
                            print(">>>INVALID INPUT. Expecting = somewhere.")
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