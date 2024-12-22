# SELECT [agg_function(agg_column) [, ... ]]
#   FROM table_name
#   [WHERE condition]
#   [GROUP_BY column_name [, ...] ];

def parse_select(prepared_input):
    prepared_input = prepared_input[prepared_input.index(" ") + 1:]  # crop function name
    if not " " in prepared_input:
        return -2  # input is lacking spaces

    # Handle aggregation start\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    if prepared_input[:6].upper() == "FROM ": # skip INTO if it is present
        prepared_input = prepared_input[6:]
        if not " " in prepared_input:
            return -2 # input is lacking spaces
    else:
        if not "GROUP_BY" in prepared_input.upper():
            return -6 # Must not have aggregation if GROUP_BY is not present
        aggregation = {}
        end_flag = 0
        temp_a = "" # temporary string for aggregation function name
        temp = "" # temporary string for undetermined pieces of input
        counter = 0
        for symbol in prepared_input:
            counter += 1
            match symbol:
                case "(":
                    end_flag = 0
                    if temp_a:
                        return -3.1 # invalid bracket or spaces structure
                    temp_a = temp
                    temp = ""
                    continue
                case ")":
                    end_flag = 1
                    if temp_a:
                        if not temp:
                            return -3.3 # invalid bracket structure. Closing bracket was encountered too soon
                        if temp in aggregation.keys():
                            return -4 # column aggregation is already specified
                        aggregation[temp] = temp_a
                        temp = ""
                        temp_a = ""
                        continue
                    return -3.3 # invalid bracket structure. Closing bracket was encountered too soon

                case ",":
                    end_flag = 0
                    if temp_a:
                        if not temp:
                            return -5  # invalid comma placement
                        if temp in aggregation.keys():
                            return -4  # column aggregation is already specified
                        aggregation[temp] = temp_a
                        temp = ""
                        temp_a = ""
                        continue
                    return -5  # invalid comma placement

                case " ":
                    if end_flag == 1:
                        end_flag = 2
                    if end_flag == 6:
                        break
                    if not temp_a:
                        if temp:
                            temp_a = temp

                case _:
                    match symbol:
                        case "F" | "f" if end_flag == 2: end_flag = 3
                        case "R" | "r" if end_flag == 3: end_flag = 4
                        case "O" | "o" if end_flag == 4: end_flag = 5
                        case "M" | "m" if end_flag == 5: end_flag = 6
                    temp += symbol

        prepared_input = prepared_input[counter+1:] # crop prepared input from the end of FROM to the end of the string
    # Handle aggregation end///////////////////////////////////////////////////////////////////////////////////////////

    if not " " in prepared_input:
        return -2 # input is lacking spaces
    table_name = prepared_input[:prepared_input.index(" ")] # get table name
    prepared_input = prepared_input[prepared_input.index(" ") + 1:]  # crop table name

    # Handle WHERE start\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    # Handle WHERE end/////////////////////////////////////////////////////////////////////////////////////////////////


    # Handle GROUP_BY start\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    # Handle GROUP_BY end//////////////////////////////////////////////////////////////////////////////////////////////