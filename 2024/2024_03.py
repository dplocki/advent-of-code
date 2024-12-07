from typing import Generator, Iterable
import re


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def load_instructions(task_input: Iterable[str]) -> Generator[str, None, None]:
    PATTERN = r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)"

    for line in task_input:
        yield from re.findall(PATTERN, line)


def do_multiplication(multiple_operation: str) -> int:
    first_number, second_number = map(int, multiple_operation[len('mul('):-1].split(','))
    return first_number * second_number


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return sum(
        do_multiplication(multiple_operation)
        for multiple_operation in load_instructions(task_input)
        if multiple_operation.startswith('mul('))


assert solution_for_first_part('xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'.splitlines()) == 161

# The input is taken from: https://adventofcode.com/2024/day/3/input
task_input = list(load_input_file('input.03.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> int:
    result = 0
    multiplication_enabled = True

    for operation in load_instructions(task_input):
        if operation == 'don\'t()':
            multiplication_enabled = False
        elif operation == 'do()':
            multiplication_enabled = True
        else:
            if not multiplication_enabled:
                continue

            result += do_multiplication(operation)

    return result


assert solution_for_second_part("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))".splitlines()) == 48
print("Solution for the first part:", solution_for_second_part(task_input))
