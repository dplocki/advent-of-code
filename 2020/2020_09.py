from collections import deque
from itertools import combinations


def load_input_file(file_name):
    with open(file_name) as file:
        yield from (int(line.strip()) for line in file)


def solution_for_first_part(task_input: [int], preamble_size: int) -> int:

    def check_for_sum(last_numbers: [int], requested_sum: int) -> bool:
        for v1, v2 in combinations(last_numbers, 2):
            if v1 + v2 == requested_sum:
                return True

        return False


    last_numbers = deque(task_input[:preamble_size], preamble_size)
    for number in task_input[preamble_size:]:
        if not check_for_sum(last_numbers, number): 
            return number

        last_numbers.append(number)


assert solution_for_first_part([35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576], 5) == 127

# The input is taken from: https://adventofcode.com/2020/day/9/input
task_input = list(load_input_file('input.09.txt'))
print("Solution for the first part:", solution_for_first_part(task_input, 25))
