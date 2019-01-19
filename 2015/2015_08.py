import re


def load_input_file(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def calculate_the_difference_after_unescape(lines):
    for line in lines:
        memory_size = len(line)
        not_memory_size = len(re.sub(r'\\x..', '_', line[1:-1].replace('\\\\', '_').replace('\\"', '_')))

        yield memory_size - not_memory_size


# The solution is taken from: https://adventofcode.com/2015/day/8/input
print("Solution for the first part:", sum(calculate_the_difference_after_unescape(load_input_file('input.08.txt'))))
