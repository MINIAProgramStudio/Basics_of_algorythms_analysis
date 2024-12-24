# SELECT [agg_function(agg_column) [, ... ]]
#   FROM table_name
#   [WHERE condition]
#   [GROUP_BY column_name [, ...] ];

def parse_select(prepared_input):
    aggregation = False
    condition = False
    group_by_columns = False
    prepared_input = prepared_input[prepared_input.index(" ") + 1:]  # crop function name
    if not " " in prepared_input:
        return -2  # input is lacking spaces


    # Handle aggregation start\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    if prepared_input[:5].upper() == "FROM ": # skip INTO if it is present
        prepared_input = prepared_input[5:]
    else:
        if not "GROUP_BY" in prepared_input.upper():
            return -6 # Must not have aggregation if GROUP_BY is not present
        aggregation = []
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
                        aggregation.append([temp_a, temp])
                        temp = ""
                        temp_a = ""
                        continue
                    return -3.3 # invalid bracket structure. Closing bracket was encountered too soon

                case ",":
                    end_flag = 0
                    if temp_a or temp:
                            return -5  # invalid comma placement
                    continue

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

        prepared_input = prepared_input[counter:] # crop prepared input from the end of FROM to the end of the string
    # Handle aggregation end///////////////////////////////////////////////////////////////////////////////////////////
    if " " in prepared_input:
        table_name = prepared_input[:prepared_input.index(" ")] # get table name
        prepared_input = prepared_input[prepared_input.index(" ") + 1:]  # crop table name
    else:
        table_name = prepared_input
        return [table_name, aggregation, condition, group_by_columns]

    # Handle WHERE start\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    if prepared_input[:6].upper() == "WHERE ":
        prepared_input = prepared_input[6:]
        condition = ["","",""]
        c = 0
        # get column_1:
        while prepared_input[c].isalpha() or prepared_input[c].isdigit() or prepared_input[c] == "_":
            condition[0] += prepared_input[c]
            c += 1
        prepared_input = prepared_input[c:]
        if prepared_input[0] == " ":
            prepared_input = prepared_input[1:]

        action = prepared_input[0]
        if not action in "=<>":
            return -7 # no comparasion sign found

        condition[2] = action

        prepared_input = prepared_input[1:]
        while prepared_input[0] == " ":
            prepared_input = prepared_input[1:]

        end_symbol = " "
        c = 0
        for symbol in prepared_input:
            c += 1
            if symbol == end_symbol:
                break
            else:
                condition[1] += symbol
        prepared_input = prepared_input[c:]
    # Handle WHERE end/////////////////////////////////////////////////////////////////////////////////////////////////

    # Handle GROUP_BY start\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    if prepared_input[:9].upper() == "GROUP_BY ":
        prepared_input = prepared_input[9:]
        group_by_columns = []
        temp = ""
        for symbol in prepared_input:
            match symbol:
                case ",":
                    if temp:
                        group_by_columns.append(temp)
                        temp = ""
                    else:
                        return -5  # invalid comma placement
                case " ":
                    continue
                case _:
                    temp += symbol
        group_by_columns.append(temp)
        temp = ""
    # Handle GROUP_BY end//////////////////////////////////////////////////////////////////////////////////////////////

    return [table_name, aggregation, condition, group_by_columns]