from functools import reduce
from operator import mul
from typing import Tuple


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def parse(task_input: str) -> Tuple[int, int]:
    return zip(*map(lambda line: tuple(map(int, line.split()[1:])), task_input.split('\n')))


def find_how_many_wins(race_time, record_distance):
    return sum(1 for _ in filter(
        lambda reached_distance: reached_distance > record_distance,
        map(
            lambda test_holding_button_time: (race_time - test_holding_button_time) * test_holding_button_time,
            range(1, race_time)
        )))


def solution_for_first_part(task_input: str) -> int:
    return reduce(mul, (find_how_many_wins(time, distance) for time, distance in parse(task_input)), 1)


example_input = '''Time:      7  15   30
Distance:  9  40  200'''

print(solution_for_first_part(example_input))
# The input is taken from: https://adventofcode.com/2023/day/6/input
task_input = load_input_file('input.06.txt')
print("Solution for the first part:",  solution_for_first_part(task_input))
