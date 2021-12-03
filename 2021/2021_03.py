from typing import List


def load_input_file(file_name: str) -> List[str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def solution_for_first_part(task_input: List[str]) -> int:
    columns_number = task_input[0]
    rows_number = len(task_input)

    gamma = ''
    epsilon = ''

    for column in range(len(columns_number)):
        zeros = sum(1 for line in task_input if line[column] == '0')
        ones = rows_number - zeros

        gamma += '0' if zeros > ones else '1'
        epsilon += '0' if zeros < ones else '1'

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
