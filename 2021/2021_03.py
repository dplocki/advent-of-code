from typing import List


ZERO = '0'
ONE = '1'


def load_input_file(file_name: str) -> List[str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def solution_for_first_part(task_input: List[str]) -> int:
    columns_number = task_input[0]
    rows_number = len(task_input)

    gamma = ''
    epsilon = ''

    for column in range(len(columns_number)):
        zeros = sum(1 for line in task_input if line[column] == ZERO)
        ones = rows_number - zeros

        gamma += ZERO if zeros > ones else ONE
        epsilon += ZERO if zeros < ones else ONE

    return int(gamma, 2) * int(epsilon, 2)


example_input = '''00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010'''.splitlines()

assert solution_for_first_part(example_input) == 198

# The input is taken from: https://adventofcode.com/2021/day/3/input
task_input = list(load_input_file('input.03.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def find_matching_line(lines: List[str], row_can_stay) -> str:
    columns_number = len(lines[0])

    for column in range(columns_number):
        lines_number = len(lines)

        zeros_count = sum(1 for line in lines if line[column] == ZERO)
        ones_count = lines_number - zeros_count

        lines = list(filter(lambda z: row_can_stay(zeros_count, ones_count, z[column]), lines))
        if len(lines) == 1:
            return lines[0]

    raise Exception('Unable to find the matching line!') 


def solution_for_second_part(task_input: List[str]) -> int:
    oxygen = find_matching_line(task_input.copy(), lambda zeros_count, ones_count, current: current == (ZERO if zeros_count > ones_count else ONE))
    co2 = find_matching_line(task_input.copy(), lambda zeros_count, ones_count, current: current == (ONE if zeros_count > ones_count else ZERO))

    return int(oxygen, 2) * int(co2, 2)


assert solution_for_second_part(example_input) == 230

print("Solution for the second part:", solution_for_second_part(task_input))
