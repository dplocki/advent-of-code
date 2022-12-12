from collections import deque
from typing import Generator, Iterable


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[str, None, None]:
    for row_index, line in enumerate(task_input):
        for column_index, c in enumerate(line):
            yield row_index, column_index, ord(c)


def solution_for_first_part(task_input: Iterable[str]) -> int:


    def get_neighbors(height_map, y, x):
        if (y, x) not in height_map:
            return

        cure = height_map[y, x]

        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            new_c = (y + dy, x + dx)
            if new_c in height_map and height_map[new_c] <= cure + 1:
                yield new_c


    height_map = {(y, x):value for y, x, value in parse(task_input)}
    start = next((y, x) for (y, x), value in height_map.items() if value == ord('S'))
    end = next((y, x) for (y, x), value in height_map.items() if value == ord('E'))
    height_map[start] = ord('a')
    height_map[end] = ord('z')

    to_check = deque([start])
    cost_so_far = {start: 0}

    while to_check:
        column_index, row_index = to_check.pop()

        if (column_index, row_index) == end:
            return cost_so_far[end]

        for new_point in get_neighbors(height_map, column_index, row_index):
            new_cost = cost_so_far[column_index, row_index] + 1

            if new_point not in cost_so_far or new_cost < cost_so_far[new_point]:
                cost_so_far[new_point] = new_cost
                to_check.appendleft(new_point)


example_input = '''Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi'''.splitlines()

assert solution_for_first_part(example_input) == 31

# The input is taken from: https://adventofcode.com/2022/day/12/input
task_input = list(load_input_file('input.12.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
