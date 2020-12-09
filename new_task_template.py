import re
import itertools
import os


def addToClipBoard(text):
    command = 'echo ' + text.strip() + '| xclip -selection clipboard'
    os.system(command)


def load_input_file(file_name):
    with open(file_name) as file:
        return file.read().strip()


def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: [str]):
    for line in task_input:
        pass

    return


def solution_for_first_part(task_input):
    lines = list(parse(task_input))


example = '''
'''.splitlines()

print(solution_for_first_part(example))
# The input is taken from: https://adventofcode.com/{year}/day/{day}/input
task_input = load_input_file('{file_input_name}')
result = solution_for_first_part(load_input_file)
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
