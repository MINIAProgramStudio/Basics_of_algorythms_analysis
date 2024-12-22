import Parser
import Data_structure

Data = Data_structure.Data()

while True:
    print()
    string = input("<<<")
    if "EXIT" in string.upper() and len(string) < 7:
        break
    if "HELP" in string.upper() and len(string) < 7:
        print(">>>List of all commands:")
        print(">EXIT -- terminates the program. Not syntax sensitive.")
        print(">HELP -- lists all avaliable commands. Not syntax sensitive.")
        print(">CREATE -- creates new table if namaspace is empty. Syntax sensitive: CREATE table_name (column_name [, ...]);")
        continue
    parsing_result = Parser.parse(Parser.prepare_input(Parser.recive_input()), Parser.commands)
    if isinstance(parsing_result, list):
        if isinstance(parsing_result[1], list):
            match parsing_result[0]:
                case "CREATE":
                    execution_result = Data.create(parsing_result[1][0],parsing_result[1][1])
                    match execution_result:
                        case 0:
                            print(">>>Table "+parsing_result[1][0]+" was created successfully.")
                        case -2:
                            print(">>>EXECUTION ERROR: CREATE. Table already exists.")
        else:
            match parsing_result[0]:
                case "CREATE":
                    match parsing_result[1]:
                        case -2:
                            print(">>>INVALID INPUT. No spaces encountered. Must be at least two spaces in CREATE.")
                        case -3.1:
                            print(">>>INVALID INPUT. No opening bracket found.")
                        case -3.2:
                            print(">>>INVALID INPUT. No closing bracket found.")
                        case -4:
                            print(">>>INVALID INPUT. Wrong comma placement")
                        case -5:
                            print(">>>INVALID INPUT. Invalid character.")

    else:
        match parsing_result:
            case -3:
                print(">>>INVALID INPUT. No spaces encountered. Must be at least one space.")
            case -2:
                print(">>>FAILED TO PARSE. No such command.")