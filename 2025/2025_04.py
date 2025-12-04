from typing import Generator, Iterable, Tuple


DIRECTIONS = set(((-1, -1), (0, -1), (1, -1), (-1, 0),  (1, 0), (-1, 1), (0, 1), (1, 1)))


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[int, int], None, None]:
    for row, line in enumerate(task_input):
        for column, character in enumerate(line):
            if character == '@':
                yield row, column


def solution_for_first_part(task_input: Iterable[str]) -> int:

    def is_accessible_by_fork(row: int, column: int) -> bool:
        count = 0

        for d_r, d_c in DIRECTIONS:
            if (row + d_r, column + d_c) in grid:
                count += 1

        return count < 4


    grid = set(parse(task_input))
    return sum(1 for r, c in grid if is_accessible_by_fork(r, c))


example_input = '''..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.'''.splitlines()

assert solution_for_first_part(example_input) == 13
# The input is taken from: https://adventofcode.com/2025/day/4/input
task_input = list(load_input_file('input.04.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
