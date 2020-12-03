from itertools import count


TREE = '#'


def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: [str]):
    for y, line in enumerate(task_input):
        yield from [(x, y) for x, c in enumerate(line) if c == TREE]


def built_counter_function(task_input: [str]):
    max_y = len(task_input)
    max_x = len(task_input[0])
    trees = list(parse(task_input))

    return lambda right, down: sum(
            1
            for x, y in zip(count(0, step=right), range(0, max_y, down))
            if (x % max_x, y) in trees
        )


def solution_for_first_part(task_input: [str]):
    return built_counter_function(task_input)(3, 1)


# The input is taken from: https://adventofcode.com/2020/day/3/input
task_input = list(load_input_file('input.03.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: [str]):
    count_trees = built_counter_function(task_input)

    return count_trees(1, 1) * count_trees(3, 1) * count_trees(5, 1) * count_trees(7, 1) * count_trees(1, 2)


print("Solution for the second part:", solution_for_second_part(task_input))
