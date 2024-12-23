# INSERT [INTO] table_name (N [, ...]);

def parse_insert(prepared_input):
    prepared_input = prepared_input[prepared_input.index(" ")+1:] # crop function name
    if not " " in prepared_input:
        return -2 # input is lacking spaces

    if prepared_input[:5].upper() == "INTO ": # skip INTO if it is present
        prepared_input = prepared_input[5:]
        if not " " in prepared_input:
            return -2 # input is lacking spaces

    table_name = prepared_input[:prepared_input.index(" ")] # get table name
    prepared_input = prepared_input[prepared_input.index(" ") + 1:]  # crop table name

    if not "(" in prepared_input:
        return -3.1  # input is lacking brackets
    if not ")" in prepared_input:
        return -3.2  # input is lacking brackets

    # parse brackets
    values = []
    temp = ""
    for symbol in prepared_input:
        match symbol:
            case ",": # if comma:
                if temp: # if temp is not empty:
                    values.append(int(temp))
                    temp = ""
                else:
                    return -4 # wrong comma placement
                continue
            case " " | "(": # if skipable:
                continue
            case ")":
                if temp: #end parsing
                    if temp == "-":
                        return -7 # no digits after minus
                    values.append(int(temp))
                    temp = ""
                break
            case _:
                if symbol.isdigit() or (not temp and symbol in ["-"]):
                    temp+=symbol
                    continue
                print(symbol)
                return -5 # invalid character
    if temp:
        return -6 # brackets were never closed
    return [table_name, values]
