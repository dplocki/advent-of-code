from itertools import zip_longest
from typing import Generator, Iterable, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def solution_for_first_part(task_input: Iterable[str]) -> int:
    snafu_digit_to_value = { '=': -2, '-': -1, '0': 0, '1': 1, '2': 2 }
    value_to_snafu_digit = {v:k for k,v in snafu_digit_to_value.items()}


    def value_to_digit_snafu(value: int) -> Tuple[str, int]:
        carrying = value // 5
        value %= 5
        if value < -2:
            value += 5
            carrying -= 1
        elif value > 2:
            value -= 5
            carrying += 1

        return value_to_snafu_digit[value], carrying


    result = ''
    carrying = 0
    for column in zip_longest(*(snafu_number[::-1] for snafu_number in task_input), fillvalue='0'):
        column_value = sum(snafu_digit_to_value[d] for d in column) + carrying
        digit, carrying = value_to_digit_snafu(column_value)
        result += digit

    while carrying:
        digit, carrying = value_to_digit_snafu(carrying)
        result += digit

    return result[::-1]


example_input = '''1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122'''.splitlines()

assert solution_for_first_part(example_input) == '2=-1=0'

# The input is taken from: https://adventofcode.com/2022/day/25/input
task_input = list(load_input_file('input.25.txt'))
result = solution_for_first_part(task_input)
print("Solution for the first part:", result)
