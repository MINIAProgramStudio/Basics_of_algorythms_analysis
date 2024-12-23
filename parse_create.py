# CREATE table_name (column_name *[INDEXED] [, ...]);

def parse_create(prepared_input):
    indexing = []
    column_names = []
    prepared_input = prepared_input[prepared_input.index(" ") + 1:]  # crop function name
    if not " " in prepared_input:
        return -2  # input is lacking spaces

    table_name = prepared_input[:prepared_input.index(" ")]  # get table name
    prepared_input = prepared_input[prepared_input.index(" ") + 1:]  # crop table name

    if not table_name[0].isalpha():
        return -5  # invalid character
    if not all([i.isalpha() or i.isdigit() or i == "_" for i in table_name]):
        return -5  # invalid character

    if not "(" in prepared_input:
        return -3.1  # input is lacking brackets
    if not ")" in prepared_input:
        return -3.2  # input is lacking brackets

    # parse brackets
    if "INDEXED" in prepared_input.upper():
        prepared_input = prepared_input[prepared_input.index("(")+1:]

        while "," in prepared_input[:prepared_input.index(")")]:
            column_name = ""
            indexed = False
            block = prepared_input[:prepared_input.index(",")]
            prepared_input = prepared_input[prepared_input.index(",")+1:]
            while block[0] == " ":
                block = block[1:]
            if " " in block:
                column_name = block[:block.index(" ")]
                block = block[block.index(" ")+1:]
                if "INDEXED " in block.upper() or block.upper()[-7:] == "INDEXED":
                    indexed = True
            else:
                column_name = block
            if not column_name[0].isalpha():
                return -5  # invalid character
            if not all([i.isalpha() for i in column_name[1:]] or [i.isdigit() for i in column_name[1:]] or [i == "_" for i in column_name[1:]]):
                return -5  # invalid character
            column_names.append(column_name)
            indexing.append(indexed)
        column_name = ""
        indexed = False
        block = prepared_input[:prepared_input.index(")")]
        while block[0] == " ":
            block = block[1:]
        if " " in block:
            column_name = block[:block.index(" ")]
            block = block[block.index(" ") + 1:]
            if "INDEXED " in block.upper() or block.upper()[-7:] == "INDEXED":
                indexed = True
        else:
            column_name = block
        if not column_name[0].isalpha():
            return -5  # invalid character
        if not all(
                [i.isalpha() for i in column_name[1:]] or [i.isdigit() for i in column_name[1:]] or [i == "_" for i in
                                                                                                     column_name[1:]]):
            return -5  # invalid character
        column_names.append(column_name)
        indexing.append(indexed)
    else:
        temp = ""
        for symbol in prepared_input:
            match symbol:
                case ",":  # if comma -- memorise column_name
                    if temp:
                        column_names.append(temp)
                        indexing.append(False)
                        temp = ""
                    else:
                        return -4  # wrong comma placement
                    continue
                case " " | "(":  # skip spaces and opening brackets
                    continue
                case ")":  # end on closing bracket
                    if temp:
                        column_names.append(temp)
                        temp = ""
                    break
                case _:  # add any other valid characters to temp
                    if symbol.isalpha() or symbol.isdigit() or symbol == "_":
                        if temp:
                            temp += symbol
                        elif symbol.isalpha():
                            temp += symbol
                        else:
                            return -5  # invalid character
                    else:
                        return -5  # invalid character
    return [table_name, column_names, indexing]



