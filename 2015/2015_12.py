import re


def load_input_file(file_name):
    with open(file_name) as file:
        return file.read().strip()


pattern = re.compile(r'-?\d+')
input = load_input_file('input.12.txt')

# The solution is taken from: https://adventofcode.com/2015/day/12/input
print("Solution for the first part:", sum(map(int, re.findall(pattern, input))))
