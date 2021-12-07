from typing import Counter


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def parse(task_input: str) -> list[int]:
    return map(int, task_input.split(','))


def find_the_best_level(task_input: str, fuel_cost_calculation) -> int:
    crabs = Counter(parse(task_input))

    lowest = min(crabs)
    higest = max(crabs)

    return min(
        sum(fuel_cost_calculation(abs(level - crab_level)) * crabs_on_level for crab_level, crabs_on_level in crabs.items())
        for level in range(lowest, higest + 1))


def solution_for_first_part(task_input: str) -> int:
    return find_the_best_level(task_input, lambda distance: distance)


example_input = '16,1,2,0,4,2,7,1,2,14'

assert solution_for_first_part(example_input) == 37

# The input is taken from: https://adventofcode.com/2021/day/7/input
task_input = load_input_file('input.07.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: str) -> int:
    return find_the_best_level(task_input, lambda distance: distance * (distance + 1) // 2)


assert solution_for_second_part(example_input) == 168
print("Solution for the second part:", solution_for_second_part(task_input))
