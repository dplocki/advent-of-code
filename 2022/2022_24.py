import heapq
from typing import Generator, Iterable, Set, Tuple
import itertools


DIRECTIONS = ((0, -1), (1, 0), (-1, 0), (0, 1), (0, 0))
BLIZZARD_MOVES = (
    ('<', 0, -1),
    ('>', 0, 1),
    ('^', -1, 0),
    ('v', 1, 0)
)

def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Tuple[Set[Tuple[str, int, int]], int, int]:
    row_size = 0
    column_size = 0

    blizzards = set()
    for row_index, line in enumerate(task_input):
        for column_index, character in enumerate(line):
            if character in '><^v':
                blizzards.add((character, row_index - 1, column_index - 1))

        column_size = column_index - 1
    row_size = row_index - 1

    return blizzards, row_size, column_size


def find_path_length(
        blizzards_map: Set[Tuple[str, int, int]],
        row_size: int,
        column_size: int,
        start_point: Tuple[int, int],
        end_point: Tuple[int, int],
        start_time: int) -> int:


    def heuristic(current_point: Tuple[int, int], time: int) -> int:
        return abs(current_point[0] - end_point[0]) + abs(current_point[1] - end_point[1]) + abs(time - start_time)


    def is_blizzard_in_coordinates(row_index: int, column_index: int, time: int) -> bool:
        return blizzards_map & set((
                d,
                (row_index - time * y) % row_size,
                (column_index - time * x) % column_size,
            ) for d, y, x in BLIZZARD_MOVES)


    def get_possibilities(row_index: int, column_index: int, time: int) -> bool:
        time += 1
        for r, c in DIRECTIONS:
            nr, nc = r + row_index, c + column_index

            if nr < 0 or nr > row_size or nc < 0 or nc > column_size:
                continue

            if not is_blizzard_in_coordinates(nr, nc, time):
                yield nr, nc, time


    for first_leave_time in itertools.count(start_time + 1):
        if not is_blizzard_in_coordinates(*start_point, first_leave_time):
            break

    to_check = [(heuristic(start_point, first_leave_time), *start_point, first_leave_time)]
    seen = set(to_check)

    while to_check:
        _, row_index, column_index, time = heapq.heappop(to_check)

        if (row_index, column_index) == end_point:
            return time + 1

        for new_row_index, new_column_index, new_time in get_possibilities(row_index, column_index, time):
            if (new_row_index, new_column_index, new_time) in seen:
                continue

            seen.add((new_row_index, new_column_index, new_time))
            heapq.heappush(
                to_check,
                (heuristic((new_row_index, new_column_index), new_time), new_row_index, new_column_index, new_time)
            )
    
    raise Exception('No path find!')


def solution_for_first_part(task_input: Iterable[str]) -> int:
    blizzards, row_size, column_size = parse(task_input)
    start_point = 0, 0
    end_point = row_size - 1, column_size - 1

    return find_path_length(blizzards, row_size, column_size, start_point, end_point, 0)


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


def solution_for_second_part(task_input: Iterable[str]) -> int:
    blizzards, row_size, column_size = parse(task_input)
    start_point = 0, 0
    end_point = row_size - 1, column_size - 1

    shortest_path_length = lambda sp, ep, st: find_path_length(blizzards, row_size, column_size, sp, ep, st)

    time1 = shortest_path_length(start_point, end_point, 0)
    time2 = shortest_path_length(end_point, start_point, time1)
    return shortest_path_length(start_point, end_point, time2)


assert solution_for_second_part(example_input) == 54
print("Solution for the second part:", solution_for_second_part(task_input))
