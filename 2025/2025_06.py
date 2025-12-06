from functools import reduce
from itertools import groupby, zip_longest
from operator import add, mul
from typing import Callable, Iterable, List


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read()


def solutions(numbers: List[List[int]], operators: List[str]) -> int:

    def get_reducer_function(operator: str) -> Callable[[int, int], int]:
        if operator == '*':
            return mul
        elif operator == '+':
            return add

        return None


    return sum(
        reduce(get_reducer_function(operator), (row[column_index] for row in numbers))
        for column_index, operator in enumerate(operators)
    )


def solution_for_first_part(lines: Iterable[str]) -> int:
    lines = lines.splitlines()
    numbers = [
        tuple(map(int, line.split()))
        for line in lines[:-1]
    ]
    operators = list(lines[-1].split())

    return solutions(numbers, operators)


example_input = '''123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  '''

assert solution_for_first_part(example_input) == 4277556
# The input is taken from: https://adventofcode.com/2025/day/6/input
task_input = load_input_file('input.06.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> int:
    lines = task_input.splitlines()
    operators = list(lines[-1].split())
    numbers_tokens = (
        ''.join(characters).strip()
        for characters in zip_longest(*lines[:-1], fillvalue=' ')
    )

    numbers = [
        list(map(int, group))
        for key, group in groupby(numbers_tokens, lambda x: x == '')
        if not key
    ]

    return solutions(list(zip(*numbers)), operators)


assert solution_for_second_part(example_input) == 3263827
print("Solution for the second part:", solution_for_second_part(task_input))
