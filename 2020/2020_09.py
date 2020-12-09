from collections import deque
from itertools import combinations


def load_input_file(file_name: str) -> [int]:
    with open(file_name) as file:
        yield from (int(line.strip()) for line in file)


def solution_for_first_part(task_input: [int], preamble_size: int) -> int:
    last_numbers = deque(task_input[:preamble_size], preamble_size)

    for number in task_input[preamble_size:]:
        if number not in map(sum, combinations(last_numbers, 2)):
            return number

        last_numbers.append(number)


assert_example = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576]
assert solution_for_first_part(assert_example, 5) == 127

# The input is taken from: https://adventofcode.com/2020/day/9/input
task_input = list(load_input_file('input.09.txt'))
first_non_maching_number = solution_for_first_part(task_input, 25)
print("Solution for the first part:", first_non_maching_number)


def solution_for_second_part(task_input: [int], request_number: int) -> int:
    numbers = list(reversed(task_input))
    contiguous_sequence = deque()

    while True:
        current_sum = sum(contiguous_sequence)
        if current_sum == request_number:
            return min(contiguous_sequence) + max(contiguous_sequence)
        elif current_sum < request_number:
            contiguous_sequence.append(numbers.pop())
        else:
            contiguous_sequence.popleft()


assert solution_for_second_part(assert_example, 127) == 62
print("Solution for the first part:", solution_for_second_part(task_input, first_non_maching_number))
