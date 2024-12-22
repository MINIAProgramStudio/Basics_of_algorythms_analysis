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
    patience = 100
    string = input()
    while not any(s in string for s in eol):
        patience -= 1
        if patience < 0:
            print("Too many new lines, exiting")
            exit()
        print(".")
        new_line = "\n"+input()
        if new_line == "\nRESET;":
            print(">>>Resetting")
            string = input()
            continue
        string += new_line
    return string

def prepare_input(string):
    i = 0
    if len(spaces) > 1:
        for space in spaces[1:]:
            while space in string:
                string.replace(space, spaces[0])
    while spaces[0] + spaces[0] in string:
        string = string.replace(spaces[0] + spaces[0], spaces[0])

    first_eol = len(string)
    for eol_s in eol:
        if string.find(eol_s)>= 0:
            first_eol = (min(string.find(eol_s),first_eol))


    return string[:first_eol]

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
        print(">>>", temp.upper())
        return -2 # no such command

    # call command-specific parser
    parsing_result = commands_dict[temp.upper()](prepared_input)
    if isinstance(parsing_result, list):
        return [temp.upper(),parsing_result]
    else:
        return [temp.upper(), parsing_result]