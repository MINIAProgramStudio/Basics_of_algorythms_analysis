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
                    if temp[0] == '"' or temp[0] == "'": # if temp is a string:
                        if temp[0] == temp[-1]: # if temp is a complete string, memorise it:
                            values.append(temp)
                            temp = ""
                        else: # if temp is not a complete string, append comma as a character:
                            temp+=symbol
                    else: # if temp is not a string, memorise it:
                        values.append(temp)
                        temp = ""
                else:
                    return -4 # wrong comma placement
                continue
            case " " | "(": # if skipable:
                if temp: # if temp is not empty:
                    if temp[0] == '"' or temp[0] == "'": # if temp is a string:
                        if temp[0] != temp[-1]: # if temp is not a complete string, append skipable as a character:
                            temp += symbol
                continue
            case ")":
                if temp: # if temp is not empty:
                    if temp[0] == '"' or temp[0] == "'": # if temp is a string:
                        if temp[0] != temp[-1]: # if temp is not a complete string, append closing bracket as a character:
                            temp += symbol
                            continue
                if temp: # otherwise end parsing
                    values.append(temp)
                    temp = ""
                break
            case _:
                if symbol.isalpha() or symbol.isdigit() or symbol in ["_", "'", '"']:
                    temp+=symbol
                    continue
                if len(temp) > 0:
                    if temp[0] == '"' or temp[0] == "'":
                        if symbol != temp[0]:
                            temp+=symbol
                            continue

                print(symbol)
                return -5 # invalid character
    if temp:
        return -6 # string was never ended
    return [table_name, values]
