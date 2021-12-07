from typing import List


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def parse(task_input: List[str]):
    return map(int, task_input.split(','))


def solution_for_first_part(task_input):
    crabs = list(parse(task_input))

    lowest = min(crabs)
    higest = max(crabs)

    return min(
        sum(abs(level - crab_level) for crab_level in crabs)
        for level in range(lowest, higest + 1))


example_input = '''16,1,2,0,4,2,7,1,2,14'''

assert solution_for_first_part(example_input) == 37

# The input is taken from: https://adventofcode.com/2021/day/7/input
task_input = load_input_file('input.07.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
