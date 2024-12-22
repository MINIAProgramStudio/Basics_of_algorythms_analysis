spaces = [' ', '\t', '\r', '\n']
string_containers = ['"', "'"]
eol = [";"]

from parse_create import parse_create

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
    "CREATE": parse_create,
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
    if not " " in prepared_input:
        return -3 # no spaces == no such command

    c = 0 # prepared_input counter

    # determine which command was inputed
    temp = ""
    while prepared_input[c] != " ":
        temp += prepared_input[c]
        c += 1

    if not temp.upper() in commands_dict.keys():
        return -2 # no such command

    # call command-specific parser
    parsing_result = commands_dict[temp.upper()](prepared_input)
    if isinstance(parsing_result, list):
        return [temp.upper()]+parsing_result
    else:
        return [temp.upper(), parsing_result]