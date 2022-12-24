import heapq
from typing import Generator, Iterable, Set, Tuple
import itertools


DIRECTIONS = ((0, -1), (1, 0), (-1, 0), (0, 1), (0, 0))


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Tuple[Set[Tuple[str, int, int]], int, int]:
    blizzards = set()
    row_size = 0
    column_size = 0

    for row_index, line in enumerate(task_input):
        for column_index, c in enumerate(line):
            if c in '><^v':
                blizzards.add((row_index - 1, column_index - 1, c))

        column_size = column_index -1
    row_size = row_index - 1

    return blizzards, row_size, column_size


def solution_for_first_part(task_input: Iterable[str]) -> int:
    blizzards_map, row_size, column_size = parse(task_input)
    BLIZZARD_MOVES = (
        ('<', 0, -1),
        ('>', 0, 1),
        ('^', -1, 0),
        ('v', 1, 0)
    )

    def heuristic(row_index: int, column_index: int, time: int) -> int:
        return abs(row_index - row_size) + abs(column_index - column_size) + time


    def is_blizzard_in_coordinates(blizzards_map: Set[Tuple[str, int, int]], row_index: int, column_index: int, time: int) -> bool:
        return blizzards_map & set((
            (row_index - time * y) % row_size,
            (column_index - time * x) % column_size,
            d) for d, y, x in BLIZZARD_MOVES)


    def get_possibilities(blizzards_map: Set[Tuple[str, int, int]], row_index: int, column_index: int, time: int) -> bool:
        time += 1
        for r, c in DIRECTIONS:
            nr, nc = r + row_index, c + column_index

            if nr < 0 or nr >= row_size or nc < 0 or nc >= column_size:
                continue

            if not is_blizzard_in_coordinates(blizzards_map, nr, nc, time):
                yield time, nr, nc


    start_point = 0, 0
    end_point = row_size - 1, column_size - 1
    for first_leave_time in itertools.count(1):
        if not is_blizzard_in_coordinates(blizzards_map, *start_point, first_leave_time):
            break

    to_check = [(heuristic(*start_point, first_leave_time), *start_point, first_leave_time)]
    seen = set(to_check)

    while to_check:
        _, row_index, column_index, time = heapq.heappop(to_check)

        if (row_index, column_index) == end_point:
            return time + 1

        for new_time, new_row_index, new_column_index in get_possibilities(blizzards_map, row_index, column_index, time):
            if (new_row_index, new_column_index, new_time) in seen:
                continue

            seen.add((new_row_index, new_column_index, new_time))
            heapq.heappush(
                to_check,
                (heuristic(new_row_index, new_column_index, new_time), new_row_index, new_column_index, new_time)
            )


example_input = '''#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#'''.splitlines()

assert solution_for_first_part(example_input) == 18

# The input is taken from: https://adventofcode.com/2022/day/24/input
task_input = list(load_input_file('input.24.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
