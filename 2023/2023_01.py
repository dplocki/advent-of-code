from typing import Generator, Iterable


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def solution_for_first_part(task_input: Iterable[str]) -> int:

    def find_first_and_last_digit(line: str) -> int:
        digits = [c for c in line if c in '0123456789']
        return int(digits[0] + digits[-1])


    return sum(find_first_and_last_digit(line) for line in task_input)


assert solution_for_first_part('''1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet'''.splitlines()) == 142

# The input is taken from: https://adventofcode.com/2023/day/1/input
task_input = list(load_input_file('input.01.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
