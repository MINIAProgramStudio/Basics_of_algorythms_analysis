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
        # parse brackets
        if command[c_c] in ["{", "[", "("]:
            bracket_level = [command[c_c]]
            c_c += 1
            while bracket_level: # while brackets are open
                # handle bracket symbols
                match command[c_c]:
                    case "{" | "[" | "(":
                        bracket_level.append(["{", "[", "("].index(command[c_c]))
                        c_c += 1
                        # bracket level errors catching:
                        if len(bracket_level) >= 2:
                            if bracket_level[-1] == bracket_level[-2]:
                                return -3.1 # example command has invalid bracket structure: can't have [[]], (()) and [[]]
                            if bracket_level[-2] == 0:
                                return -3.2  # example command has invalid bracket structure: {no brackets should be here}


                        continue
                    case "}" | "]" | ")":
                        if ["}", "]", ")"].index(command[c_c]) == bracket_level[-1]:
                            bracket_level.pop(-1)
                            c_c += 1
                            continue
                        else:
                            return -3.3 # example command has invalid bracket structure: brackets were never closed

                # handle {OPTIONAL_PHRASE_OR_WORD}
                if bracket_level[-1] == 0:
                    optional_keyword = ""
                    typed_in = True
                    old_p_c = p_c
                    while command[c_c] != "}" and c_c < len(command):
                        optional_keyword += command[c_c]
                        if typed_in:
                            if command[c_c] == prepared_input[p_c]:
                                p_c += 1
                            else:
                                p_c = old_p_c
                                typed_in = False
                        c_c += 1
                    if c_c == len(command):
                        return -3.3 # example command has invalid bracket structure: brackets were never closed
                    args[optional_keyword] = typed_in

                # handle () -- value brackets
                if bracket_level[-1] == 2:
                    if len(bracket_level) >= 2:
                        pass
                    # handle obligatory ()
                    else:
                        valid_lengths = []
                        temp = ""
                        while command[c_c] != ")" and c_c < len(command):
                            match command[c_c]:
                                case " ":
                                    if temp:
                                        valid_lengths.append(int(temp))
                                case _:
                                    temp += command[c_c]
                            c_c += 1
                        if c_c == len(command):
                            return -3.3  # example command has invalid bracket structure: brackets were never closed

                        # parse input
                        temp = ""
                        values = [[]]
                        while prepared_input[p_c] != ")" and p_c < len(prepared_input):
                            match prepared_input[p_c]:
                                case "(":
                                    p_c += 1
                                case " ":
                                    if temp:
                                        values[-1].append(temp)
                                        temp = ""
                                case ",":
                                    if temp:
                                        values[-1].append(temp)
                                        temp = ""
                                    values.append([])
                        
                                    


        # parse keywords
        if (command[c_c].isalpa() or command[c_c] == "_") and command[c_c] == command[c_c].upper():
            while command[c_c] == prepared_input[p_c].uppercase():  # while input matches keyword
                c_c += 1
                p_c += 1
            if command[c_c] != " ":
                return -4 # optional keyword missing/entered wrong

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