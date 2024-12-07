from typing import Generator, Iterable
import re


PATTERN = r"mul\(\d{1,3},\d{1,3}\)"


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def solution_for_first_part(task_input: Iterable[str]) -> int:
    result = 0

    for line in task_input:
        for multiple_operation in re.findall(PATTERN, line):
            first_number, second_number = map(int, multiple_operation[len('mul('):-1].split(','))
            result += first_number * second_number

    return result


example_input = '''xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'''.splitlines()

assert solution_for_first_part(example_input) == 161

# The input is taken from: https://adventofcode.com/2024/day/3/input
task_input = list(load_input_file('input.03.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
