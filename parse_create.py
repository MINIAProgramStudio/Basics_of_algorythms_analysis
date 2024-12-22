# CREATE table_name (column_name *[INDEXED] [, ...]);

def parse_create(prepared_input):
    prepared_input = prepared_input[prepared_input.index(" ")+1:] # crop function name
    if not " " in prepared_input:
        return -2 # input is lacking spaces

    table_name = prepared_input[:prepared_input.index(" ")] # get table name
    prepared_input = prepared_input[prepared_input.index(" ") + 1:]  # crop table name

    if not " " in prepared_input:
        return -2  # input is lacking spaces
    if not "(" in prepared_input:
        return -3.1  # input is lacking brackets
    if not ")" in prepared_input:
        return -3.2  # input is lacking brackets

    # parse brackets
    column_names = []
    temp = ""
    for symbol in prepared_input:
        match symbol:
            case ",":
                if temp:
                    column_names.append(temp)
                    temp = ""
                else:
                    return -4 # wrong comma placement
            case " ":
                continue
            case ")":
                if temp:
                    column_names.append(temp)
                    temp = ""
                break
            case _:
                if symbol.isalpha() or symbol == " ":
                    temp+=symbol
                else:
                    return -5 # invalid character
    return (table_name, [column_names])


