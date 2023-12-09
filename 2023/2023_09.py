from functools import reduce
from typing import Callable, Generator, Iterable, Tuple
from itertools import pairwise


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple, None, None]:
    for line in task_input:
        yield tuple(map(int, line.split(' ')))


def build_pyramid(numbers: Tuple[int, ...]) -> Generator[Tuple, None, None]:
    yield numbers

    while any(number != 0 for number in numbers):
        new_numbers = tuple((b - a) for a, b in pairwise(numbers))
        yield new_numbers
        numbers = new_numbers


def find_value_for_first_part(numbers: Tuple[int, ...]) -> int:
    return sum(line[-1] for line in build_pyramid(numbers))


def solution(task_input: Iterable[str], find_value_for: Callable[[str], int]) -> int:
    return sum(find_value_for(line) for line in parse(task_input))


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return solution(task_input, find_value_for_first_part)


example_input = '''0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45'''.splitlines()

assert solution_for_first_part(example_input) == 114

# The input is taken from: https://adventofcode.com/2023/day/9/input
task_input = list(load_input_file('input.09.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def find_value_for_second_part(numbers: Tuple[int, ...]) -> int:
    pyramid = list(build_pyramid(numbers))
    return reduce(lambda result, line: line[0] - result, pyramid[::-1], 0)


def solution_for_second_part(task_input: Iterable[str]) -> int:
    return solution(task_input, find_value_for_second_part)


assert solution_for_second_part(example_input) == 2
print("Solution for the second part:", solution_for_second_part(task_input))
