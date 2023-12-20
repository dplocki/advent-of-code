from typing import Generator, Iterable, List
import re
import itertools
import os
import collections


def addToClipBoard(text) -> None:
    command = 'echo ' + str(text).strip() + '| xclip -selection clipboard'
    os.system(command)


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]):
    for line in task_input:
        line

    return


def solution_for_first_part(task_input: Iterable[str]) -> int:
    lines = list(parse(task_input))


example_input = ''''''.splitlines()

print(solution_for_first_part(example_input))
# The input is taken from: https://adventofcode.com/{year}/day/{day}/input
task_input = list(load_input_file('{file_input_name}'))
result = solution_for_first_part(task_input)
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


def visualization(point_dictionary):
    rows = [row for row, column in point_dictionary.keys()]
    columns = [column for row, column in point_dictionary.keys()]
    max_rows = max(rows)
    max_columns = max(columns)
    min_rows = min(rows)
    min_columns = min(columns)

    for row in range(min_rows, max_rows + 1):
        for column in range(min_columns, max_columns + 1):
            print(point_dictionary[row, column], end='')

        print()


# 4 - direction
# [(0, -1), (1, 0), (-1, 0), (0, 1)]

# 8 - direction
# [(-1, -1), (0, -1), (1, -1), (-1, 0),  (1, 0), (-1, 1), (0, 1), (1, 1)]

def bfs(_map, get_neighbors, start, end):
    to_check = collections.deque([start])
    cost_so_far = dict()
    cost_so_far[start] = 0

    while to_check:
        column_index, row_index = to_check.pop()

        if (column_index, row_index) == end:
            return cost_so_far[end]

        for new_point in get_neighbors(_map, column_index, row_index):
            new_cost = cost_so_far[column_index, row_index] + 1

            if new_point not in cost_so_far or new_cost < cost_so_far[new_point]:
                cost_so_far[new_point] = new_cost
                to_check.appendleft(new_point)
