from itertools import count


TREE = '#'


def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: [str]):
    for y, line in enumerate(task_input):
        yield from [(x, y) for x, c in enumerate(line) if c == TREE]


def solution_for_first_part(task_input: [str]):
    max_y = len(task_input)
    max_x = len(task_input[0])
    trees = list(parse(task_input))

    return sum(
            1
            for x, y in zip(count(0, step=3), range(0, max_y))
            if (x % max_x, y) in trees
        )

# The input is taken from: https://adventofcode.com/2020/day/3/input
task_input = list(load_input_file('input.03.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
