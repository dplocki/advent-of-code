from typing import List


MAXIUM_LIFE_SPAN = 8
RESET_TO_VALUE = 6


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def parse(task_input: List[str]):
    return map(int, task_input.split(','))


def lanternfish_symulator(task_input: str, simulation_run: int) -> int:
    initial_population = list(parse(task_input))

    population = {timer:initial_population.count(timer) for timer in range(MAXIUM_LIFE_SPAN)}

    for _ in range(simulation_run):
        new_population = {(timer - 1):count for timer, count in population.items()}

        if -1 in new_population:
            new_population[MAXIUM_LIFE_SPAN] = new_population[-1]
            new_population[RESET_TO_VALUE] = new_population.get(RESET_TO_VALUE, 0) + new_population[-1]
            new_population[-1] = 0

        population = new_population

    return sum(v for v in population.values())


def solution_for_first_part(task_input: List[str]) -> int:
    return lanternfish_symulator(task_input, 80)


example_input = '3,4,3,1,2'
assert solution_for_first_part(example_input) == 5934

# The input is taken from: https://adventofcode.com/2021/day/6/input
task_input = load_input_file('input.06.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: List[str]) -> int:
    return lanternfish_symulator(task_input, 256)


assert solution_for_second_part(example_input) == 26984457539

print("Solution for the second part:", solution_for_second_part(task_input))