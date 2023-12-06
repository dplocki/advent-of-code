from functools import reduce
from operator import mul
from typing import Tuple
from math import floor, ceil


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def parse_for_first_task(task_input: str) -> Tuple[int, int]:
    return zip(*map(lambda line: tuple(map(int, line.split()[1:])), task_input.split('\n')))


def find_how_many_wins(race_time: int, record_distance: int) -> int:
    part_under_the_square = (race_time ** 2 - 4 * record_distance) ** 0.5

    t1 = ceil((race_time + part_under_the_square) / 2)
    t2 = floor((race_time - part_under_the_square) / 2)

    return t1 - t2 - 1


def solution_for_first_part(task_input: str) -> int:
    return reduce(mul, (find_how_many_wins(time, distance) for time, distance in parse_for_first_task(task_input)), 1)


example_input = '''Time:      7  15   30
Distance:  9  40  200'''

assert solution_for_first_part(example_input) == 288
# The input is taken from: https://adventofcode.com/2023/day/6/input
task_input = load_input_file('input.06.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


def parse_for_second_task(task_input: str) -> Tuple[int, int]:
    return tuple(
        map(
            lambda line: int(''.join(character for character in line if character.isnumeric())),
            task_input.split('\n')
        ))


def solution_for_second_part(task_input: str) -> int:
    return find_how_many_wins(*parse_for_second_task(task_input))


assert solution_for_second_part(example_input) == 71503
print("Solution for the second part:",  solution_for_second_part(task_input))
