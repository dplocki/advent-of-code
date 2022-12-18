import itertools
from typing import Generator, Iterable, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]):
    for line in task_input:
        yield tuple(map(int, line.split(',')))


def manhattan_distance(point1: Tuple[int, ...], point2: Tuple[int, ...]) -> int:
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1]) + abs(point1[2] - point2[2])


def solution_for_first_part(task_input: Iterable[str]) -> int:
    cubes = set(parse(task_input))
    result = len(cubes) * 6

    for c1, c2 in itertools.combinations(cubes, 2):
        if manhattan_distance(c1, c2) == 1:
            result -= 2

    return result


example_input = '''2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5'''.splitlines()

assert solution_for_first_part(example_input) == 64
# The input is taken from: https://adventofcode.com/2022/day/18/input
task_input = list(load_input_file('input.18.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
