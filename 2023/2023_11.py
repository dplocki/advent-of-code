from typing import Generator, Iterable, Set
import itertools


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Set[tuple[int, int]]:
    return set(
        (row_index, column_index)
        for row_index, line in enumerate(task_input)
        for column_index, character in enumerate(line)
        if character == '#')


def solution_for_first_part(task_input: Iterable[str]) -> int:
    stars = parse(task_input)
    star = next(iter(stars))
    minimal_row = maximal_row = star[0]
    minimal_column = maximal_column = star[1]
    rows_with_stars = set()
    columns_with_stars = set()

    for star in stars:
        minimal_row = min(star[0], minimal_row)
        minimal_column = min(star[1], minimal_column)
        maximal_row = max(star[0], maximal_row)
        maximal_column = max(star[1], maximal_column)
        rows_with_stars.add(star[0])
        columns_with_stars.add(star[1])

    rows_to_extend = set(range(minimal_row, maximal_row + 1)).difference(rows_with_stars)
    columns_to_extend = set(range(minimal_column, maximal_column + 1)).difference(columns_with_stars)

    extended_stars_map = set()
    for star in stars:
        row_modification = sum(1 for r in rows_to_extend if r < star[0])
        column_modification = sum(1 for c in columns_to_extend if c < star[1])
        extended_stars_map.add((star[0] + row_modification, star[1] + column_modification))

    return sum(
        abs(star_a[0] - star_b[0]) + abs(star_a[1] - star_b[1])
        for star_a, star_b in itertools.combinations(extended_stars_map, 2))


example_input = '''...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....'''.splitlines()

assert solution_for_first_part(example_input) == 374

# The input is taken from: https://adventofcode.com/2023/day/11/input
task_input = list(load_input_file('input.11.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
