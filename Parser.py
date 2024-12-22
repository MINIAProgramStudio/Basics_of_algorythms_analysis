spaces = [' ', '\t', '\r', '\n']
string_containers = ['"', "'"]
eol = [";"]

from parse_create import parse_create
from parse_insert import parse_insert
from parse_select import parse_select

import sys

commands = {
    "CREATE": parse_create,
    "INSERT": parse_insert,
    "SELECT": parse_select
}

def recive_input():
    string = str(sys.stdin.buffer.readline())
    while not any(s in string for s in eol):
        new_line = "\n"+input("...")
        if new_line == "\nRESET;":
            print(">>>Resetting")
            string = sys.stdin.buffer.readline()
            continue
        string += new_line
    return string[2:]

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
        return [temp.upper(),parsing_result]
    else:
        return [temp.upper(), parsing_result]