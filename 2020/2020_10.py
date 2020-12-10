from collections import Counter


def load_input_file(file_name: str):
    with open(file_name) as file:
        yield from (int(line.strip()) for line in file)


def solution_for_first_part(task_input: [int]) -> int:
    jolts = sorted(task_input)
    results = Counter(
        b - a
        for a, b in zip([0] + jolts, jolts + [jolts[-1] + 3])
    )

    return results[1] * results[3]


example_input = [28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3]
assert solution_for_first_part(example_input) == 220 

# The input is taken from: https://adventofcode.com/2020/day/10/input
print("Solution for the first part:", solution_for_first_part(load_input_file('input.10.txt')))
