from typing import Generator, Iterable, Tuple
import itertools


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[int, int], None, None]:
    for line in task_input:
        yield tuple(map(int, line.split(',')))


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return max(
        (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)
    for  a, b in itertools.combinations(parse(task_input), 2))


example_input = '''7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3'''.splitlines()

assert solution_for_first_part(example_input) == 50
# The input is taken from: https://adventofcode.com/2025/day/9/input
task_input = list(load_input_file('input.09.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
