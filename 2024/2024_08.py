from typing import Dict, Generator, Iterable, Tuple
import itertools


ROW = 0
COLUMN = 1


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Tuple[Dict[Tuple[int, int], int]]:
    rows = 0
    antennas_map = {}

    for row, line in enumerate(task_input):
        columns = len(task_input[0])
        rows += 1

        for column, character in enumerate(line):
            if character != '.':
                antennas_map[row, column] = character

    return antennas_map, (rows, columns)


def antinode_fits_to_size(size: Tuple[int, int], location: Tuple[int, int]) -> bool:
    return 0 <= location[ROW] < size[ROW] and 0 <= location[COLUMN] < size[COLUMN]


def solution(antinode_generator: Generator[Tuple[int, int], None, None], task_input: Iterable[str]) -> int:
    antenna_map, size = parse(task_input)
    solutions = set()

    for antenna_a, antenna_b in itertools.combinations(antenna_map.keys(), r=2):
        if antenna_map[antenna_a] != antenna_map[antenna_b]:
            continue

        for antinode in antinode_generator(size, antenna_a, antenna_b):
            solutions.add(antinode)

    return len(solutions)


def solution_for_first_part(task_input: Iterable[str]) -> int:

    def antinode_generator(size, antenna_a, antenna_b):
        is_matched = lambda location: antinode_fits_to_size(size, location)

        d_row = antenna_b[ROW] - antenna_a[ROW]
        d_column = antenna_b[COLUMN] - antenna_a[COLUMN]

        antinode_a = antenna_a[ROW] - d_row, antenna_a[COLUMN] - d_column
        antinode_b = antenna_b[ROW] + d_row, antenna_b[COLUMN] + d_column

        if is_matched(antinode_a):
            yield antinode_a

        if is_matched(antinode_b):
            yield antinode_b


    return solution(antinode_generator, task_input)


example_input = '''............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............'''.splitlines()

assert solution_for_first_part(example_input) == 14

# The input is taken from: https://adventofcode.com/2024/day/8/input
task_input = list(load_input_file('input.08.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> int:

    def antinode_generator(size, antenna_a, antenna_b):
        is_matched = lambda location: antinode_fits_to_size(size, location)

        yield antenna_a
        yield antenna_b

        d_row = antenna_b[ROW] - antenna_a[ROW]
        d_column = antenna_b[COLUMN] - antenna_a[COLUMN]

        antinode_a = antenna_a[ROW] - d_row, antenna_a[COLUMN] - d_column
        antinode_b = antenna_b[ROW] + d_row, antenna_b[COLUMN] + d_column

        while True:
            exit_a, exit_b = False, False

            if is_matched(antinode_a):
                yield antinode_a
            else:
                exit_a = True

            if is_matched(antinode_b):
                yield antinode_b
            else:
                exit_b = True

            if exit_a and exit_b:
                return

            antinode_a = antinode_a[ROW] - d_row, antinode_a[COLUMN] - d_column
            antinode_b = antinode_b[ROW] + d_row, antinode_b[COLUMN] + d_column

    return solution(antinode_generator, task_input)


assert solution_for_second_part(example_input) == 34
print("Solution for the second part:", solution_for_second_part(task_input))
