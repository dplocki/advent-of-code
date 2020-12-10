import re
import itertools
import os
import collections
import functools


def addToClipBoard(text) -> None:
    command = 'echo ' + str(text).strip() + '| xclip -selection clipboard'
    os.system(command)


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def load_input_file(file_name: str) -> [str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: [str]):
    for line in task_input:
        pass

    return


def solution_for_first_part(task_input):
    lines = list(parse(task_input))


example_input = '''
'''.splitlines()

print(solution_for_first_part(example_input))
# The input is taken from: https://adventofcode.com/{year}/day/{day}/input
task_input = list(load_input_file('{file_input_name}'))
result = solution_for_first_part(load_input_file(task_input))
print("Solution for the first part:", result)
addToClipBoard(result)


def visualization(point_dictionary):
    xs = [x for x, _ in point_dictionary.keys()]
    ys = [y for _, y in point_dictionary.keys()]
    max_x = max(xs)
    max_y = max(ys)
    min_x = min(xs)
    min_y = min(ys)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print(point_dictionary[x, y], end='')

        print()
