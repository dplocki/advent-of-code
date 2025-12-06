from functools import reduce
from operator import add, mul
from typing import Callable, Generator, Iterable, Union


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Union[int, str], None, None]:
    task_input = list(task_input)
    for line in task_input[:-1]:
        yield list(map(int, line.split()))

    yield list(task_input[-1].split())


def solution_for_first_part(task_input: Iterable[str]) -> int:

    def get_reducer_function(operator: str) -> Callable[[int, int], int]:
        if operator == '*':
            return mul
        elif operator == '+':
            return add

        return None


    matrix = list(parse(task_input))
    return sum(
        reduce(get_reducer_function(operator), (row[column_index] for row in matrix[:-1]))
        for column_index, operator in enumerate(matrix[-1])
    )


example_input = '''123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  '''.splitlines()

assert solution_for_first_part(example_input) == 4277556
# The input is taken from: https://adventofcode.com/2025/day/6/input
task_input = list(load_input_file('input.06.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
