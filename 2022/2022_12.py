from collections import deque
from typing import Dict, Generator, Iterable, List, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def build_height_map(task_input: Iterable[str]) -> Tuple[Dict[Tuple[int, int], int], Tuple[int, int], Tuple[int, int]]:

    def parse(task_input: Iterable[str]) -> Generator[str, None, None]:
        for row_index, line in enumerate(task_input):
            for column_index, c in enumerate(line):
                yield row_index, column_index, ord(c)

    height_map = {(y, x):value for y, x, value in parse(task_input)}
    start = next((y, x) for (y, x), value in height_map.items() if value == ord('S'))
    end = next((y, x) for (y, x), value in height_map.items() if value == ord('E'))
    height_map[start] = ord('a')
    height_map[end] = ord('z')

    return height_map, start, end


def solution(height_map: Dict[Tuple[int, int], int], starting: List[Tuple[int, int]], end) -> int:


    def get_neighbors(height_map, y, x):
        current_height = height_map[y, x]

        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            neighbor = (y + dy, x + dx)
            if neighbor in height_map and height_map[neighbor] <= current_height + 1:
                yield neighbor


    to_check = deque(starting)
    cost_so_far = {start:0 for start in starting}

    while to_check:
        column_index, row_index = to_check.pop()

        if (column_index, row_index) == end:
            yield cost_so_far[end]
            continue

        for new_point in get_neighbors(height_map, column_index, row_index):
            new_cost = cost_so_far[column_index, row_index] + 1

            if new_point not in cost_so_far or new_cost < cost_so_far[new_point]:
                cost_so_far[new_point] = new_cost
                to_check.appendleft(new_point)


def solution_for_first_part(task_input: Iterable[str]) -> int:
    height_map, start, end = build_height_map(task_input)

    return next(solution(height_map, [start], end))


example_input = '''Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi'''.splitlines()

assert solution_for_first_part(example_input) == 31

# The input is taken from: https://adventofcode.com/2022/day/12/input
task_input = list(load_input_file('input.12.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> int:
    height_map, _, end = build_height_map(task_input)
    starting = [(y, x) for (y, x), value in height_map.items() if value == ord('a')]

    return min(solution(height_map, starting, end))


assert solution_for_second_part(example_input) == 29
print("Solution for the second part:", solution_for_second_part(task_input))
