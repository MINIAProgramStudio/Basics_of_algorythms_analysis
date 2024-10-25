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
    "CREATE": "CREATE table_name (1 , 2)",
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
