import json
import re


def load_input_file(file_name):
    with open(file_name) as file:
        return file.read().strip()


pattern = re.compile(r'-?\d+')

# The input is taken from: https://adventofcode.com/2015/day/12/input
json_data = load_input_file('input.12.txt')

print("Solution for the first part:", sum(map(int, re.findall(pattern, json_data))))


def return_value(o) -> int:
    if type(o) is list:
        return sum(map(return_value, o))
    elif type(o) is dict:
        values = o.values()
        return 0 if "red" in values else sum(map(return_value, values))
    elif type(o) is str:
        return 0
    else:
        return o


print("Solution for the second part:", return_value(json.loads(json_data)))
