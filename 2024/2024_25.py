from typing import Iterable, Tuple


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def transpose(matrix: Iterable[Iterable]) -> Iterable[Iterable]:
    return zip(*matrix, strict=True)


def parse(task_input: Iterable[str]) -> Tuple[Iterable[Tuple[int, int, int, int, int]], Iterable[Tuple[int, int, int, int, int]]]:
    locks = []
    keys = []

    for schema in task_input.split('\n\n'):
        transposed_schema = tuple(line.count('#') -1 for line in transpose(schema.splitlines()))

        if schema.startswith('#####'):
            locks.append(transposed_schema)
        elif schema.endswith('#####'):
            keys.append(transposed_schema)

    return locks, keys


def solution_for_first_part(task_input: Iterable[str]) -> int:
    locks, keys = parse(task_input)

    return sum(
        1
        for key in keys
        for lock in locks
        if all(k + l <= 5 for k, l in zip(key, lock)))


example_input = '''#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####'''

assert solution_for_first_part(example_input) == 3

# The input is taken from: https://adventofcode.com/2024/day/25/input
task_input = load_input_file('input.25.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
