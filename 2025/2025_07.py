from typing import Generator, Iterable, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]):
    for row, line in enumerate(task_input):
        for column, character in enumerate(line):
            if character != '.':
                yield row, column, character


def solution_for_first_part(task_input: Iterable[str]) -> int:
    splitters = set()
    start = None
    rows_number = 0

    for current_row, column, character in parse(task_input):
        if character == 'S':
            start = current_row, column
        else:
            splitters.add((current_row, column))

        rows_number = max(rows_number, current_row)

    current_row = start[0]
    points = set([start])
    result = 0

    while current_row <= rows_number:
        new_points = set()

        for current_row, column in points:
            new_point = (current_row + 1, column)

            if new_point in splitters:
                new_points.add((current_row + 1, column - 1))
                new_points.add((current_row + 1, column + 1))
                result += 1
            else:
                new_points.add(new_point)

        points = new_points
        current_row += 1

    return result


example_input = '''.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............'''.splitlines()

assert solution_for_first_part(example_input) == 21
# The input is taken from: https://adventofcode.com/2025/day/7/input
task_input = list(load_input_file('input.07.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
