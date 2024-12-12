spaces = [' ', '\t', '\r', '\n']
string_containers = ['"', "'"]
eol = [";"]


"""
command syntax:
Must start with COMMAND_CAPITAL_NAME
Followed by other syntax structures:
OBLIGATORY_KEYWORD
{OPTIONAL_PHRASE_OR_WORD} # Parser will return True if this was inputted or False otherwise
value 
(n_of_vals_1, n_of_vals_2, ..., leave empty for any number of values between commas) # Parser will return list of lists of values
[OPTIONAL_KEYWORD (n_of_vals_b_c_1,n_of_vals_b_c_2,...,leave empty for any number of values between commas)] # Parser will return list of lists of values or None if keyword was not present



"COMMAND_CAPITAL_NAME": "COMMAND_NAME {OPTIONAL_PHRASE_OR_WORD} value [OPTIONAL_KEYWORD value]"
"""

commands = {
    "CREATE": "CREATE table_name (1, 2)",
    "INSERT": "INSERT {INTO} table_name (1)",
    "SELECT": "SELECT [(1)] FROM table_name [WHERE condition] [GROUP_BY (1)]"
}

def recive_input():
    string = input(">>>")
    while not any(s in string for s in eol):
        new_line = "\n"+input("...")
        if new_line == "\nRESET;":
            print("<<<Resetting")
            string = input(">>>")
            continue
        string += new_line
    return string

def prepare_input(string):
    i = 0
    while i < len(string):
        if string[i] in spaces:
            string = string[:i] + spaces[0] + string[i+1:]
            if i > 0:
                if string[i-1] == string[i]:
                    string = string[:i-1]+string[i:]
                    continue
        if string[i] in eol:
            string = string[:i]
            break
        i+=1
    return string

def parse(prepared_input, commands_dict):
    p_c = 0 # prepared_input counter
    c_c = 0 # command counter

    # determine which command was inputed
    p_temp = ""
    while prepared_input[p_c] != " ":
        p_temp += prepared_input[p_c]
        p_c += 1

    if not p_temp.upper() in commands_dict.keys():
        return -2 # no such command

    args = {}
    args["command"] = p_temp.upper()
    command = commands_dict[p_temp.upper()]
    c_c = p_c

    # skip space
    p_c += 1
    c_c += 1

    # while command is not parsed fully
    while c_c < len(command):
        # skip optional keywords
        if command[c_c] == "{":
            temp = ""
            p_c_old = p_c
            c_c += 1
            while command[c_c] == prepared_input[p_c].uppercase(): # while input matches optional keyword/phrase
                temp += command[c_c]
                c_c += 1
                p_c += 1
            if command[c_c] == "}": # if fully matched
                c_c += 2 # skip "} "
                args[temp] = True
            else:
                while command[c_c] != "}":
                    temp += command[c_c]
                    c_c += 1
                c_c += 2
                args[temp] = False
                p_c = p_c_old

        # parse obligatory keywords
        if command[c_c].isalpha() and command[c_c] == command[c_c].upper():
            while command[c_c] == prepared_input[p_c].uppercase():  # while input matches obligatory keyword
                c_c += 1
                p_c += 1
            if command[c_c] != " ":
                return -3 # optional keyword missing/entered wrong

        # parse obligatory values
        if command[c_c].isalpha() and command[c_c] == command[c_c].lower():
            temp_c = ""
            temp_p = ""
            while prepared_input[p_c] != " ": # get value
                temp_p += prepared_input[p_c]
                p_c += 1
            while command[c_c] != " ": # get name of the value
                temp_c += command[c_c]
                c_c += 1
            args[temp_c] = temp_p # store value
            # skip space
            p_c += 1
            c_c += 1

        # parse brackets
        if command[c_c] == "(":
            c_c += 1
            if command[c_c] == ")": # any number of values between commas
                brackets = [[]]
                temp = ""
                while prepared_input[p_c] != ")":
                    if p_c == len(prepared_input)-1:
                        return -4 # brackets were never closed
                    match prepared_input[p_c]:
                        case " " if temp != "": # if value exists
                                brackets[-1].append(temp)
                                temp = ("")
                        case ",":  # if value exists
                            if temp != "":
                                brackets[-1].append(temp)
                            brackets.append([])
                            temp = ("")
                        case _:
                            temp += prepared_input[p_c]
                    p_c += 1
                if "obligatory_brackets" in args.keys():
                    args["obligatory_brackets"].append(brackets)
                else:
                    args["obligatory_brackets"] = [brackets]
            else:
                # get valid lengths
                lengths  = []
                temp = ""
                while command[c_c] != ")":
                    match command[c_c]:
                        case "," | " " if temp != "":
                                lengths.append(int(temp))
                                temp = ""
                        case _ if command[c_c].isdigit():
                            temp+=command[c_c]
                    c_c += 1

                # parse brackets
                brackets = [[]]
                temp = ""
                while prepared_input[p_c] != ")":
                    if p_c == len(prepared_input)-1:
                        return -4 # brackets were never closed
                    match prepared_input[p_c]:
                        case " " if temp != "":  # if value exists
                            brackets[-1].append(temp)
                            temp = ("")
                        case ",":  # if value exists
                            if temp != "":
                                brackets[-1].append(temp)
                            if not len(brackets[-1]) in lengths:
                                return -5 # invalid number of values between commas
                            brackets.append([])
                            temp = ("")
                        case _:
                            temp += prepared_input[p_c]
                    p_c += 1
                if "obligatory_brackets" in args.keys():
                    args["obligatory_brackets"].append(brackets)
                else:
                    args["obligatory_brackets"] = [brackets]
            # skip space
            p_c += 1
            c_c += 1
