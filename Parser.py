spaces = [' ', '\t', '\r', '\n']
string_containers = ['"', "'"]
eol = [";"]


"""
command checker syntax:
Must start with COMMAND_CAPITAL_NAME
Followed by other syntax structures:
OBLIGATORY_KEYWORD
{OPTIONAL_PHRASE_OR_WORD} # Parser will return True if this was inputted or False otherwise
(n_of_vals_1, n_of_vals_2, ..., leave empty for any number of values between commas) # Parser will return list of lists of values
[OPTIONAL_KEYWORD (n_of_vals_b_c_1, n_of_vals_b_c_2, ..., leave empty for any number of values between commas)] # Parser will return list of lists of values or None if keyword was not present



"COMMAND_CAPITAL_NAME": "COMMAND_NAME {OPTIONAL_PHRASE_OR_WORD} [OPTIONAL_KEYWORD value]"
"""

commands = {
    "CREATE": "CREATE table_name (1, 2)",
    "INSERT": "INSERT {INTO} table_name (1)",
    "SELECT": "SELECT [(1)] FROM table_name [WHERE condition] [GROUP_BY (1)}"
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
    if prepared_input[0] in commands_dict.keys():
        args = {}
        command = commands_dict[prepared_input[0]]
        p_counter = 0
        c_counter = 0
        while p_counter < len(prepared_input):
            temp = ""
            while c_counter<len(command):
                match command[c_counter]:
                    case " ":
                        break
                    case _:
                        temp += command[c_counter]
                        c_counter += 1
            if temp.upper() == temp:
                if prepared_input[p_counter] == temp:
                    p_counter += 1
                    c_counter += 1
                    continue
                elif temp[0] == "{" and temp[-1] == "}":
                    if prepared_input[p_counter] == temp[1:-1]:
                        args[temp[1:-1]] = True
                    else:
                        args[temp[1:-1]] = False
                elif temp[0] == "[" or temp[-1] in [")","]","}"]:
                    pass
                else:
                    return -2
            if temp.lower() == temp:
                args[temp] = prepared_input[p_counter]
                p_counter += 1
                c_counter += 1
                continue

            if temp[0] == "(" and temp[-1] == ")":
                if len(temp) > 2:
                    lengths = []
                    br_temp = ""
                    for symbol in temp:
                        match symbol:
                            case "(":
                                continue
                            case ",":
                                lengths.append(int(br_temp))
                            case " ":
                                continue
                            case ")":
                                lengths.append(int(br_temp))
                            case _:
                                br_temp+=symbol




    else:
        return -1