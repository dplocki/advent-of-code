from typing import Generator, List, Tuple
from enum import Enum


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: List[str]) -> Generator[Tuple[str, str], None, None]:
    for line in task_input:
        yield line.split(' ')


def result_of_match(opponent: Shape, me: Shape) -> int:
    if (opponent == Shape.ROCK and me == Shape.ROCK) or \
       (opponent == Shape.PAPER and me == Shape.PAPER) or \
       (opponent == Shape.SCISSORS and me == Shape.SCISSORS):
        return 3

    if (opponent == Shape.ROCK and me == Shape.PAPER) or \
       (opponent == Shape.PAPER and me == Shape.SCISSORS) or \
       (opponent == Shape.SCISSORS and me == Shape.ROCK):
        return 6

    return 0


def solution_for_first_part(task_input):
    lines = parse(task_input)

    opponent_convert_table = {
        'A': Shape.ROCK,
        'B': Shape.PAPER,
        'C': Shape.SCISSORS
    }

    mine_convert_table = {
        'X': Shape.ROCK,
        'Y': Shape.PAPER,
        'Z': Shape.SCISSORS
    }

    result = 0
    for opponent, me in lines:
        mine_choice = mine_convert_table[me]
        result += mine_choice.value + result_of_match(opponent_convert_table[opponent], mine_choice)

    return result


example_input = '''A Y
B X
C Z'''.splitlines()

assert solution_for_first_part(example_input) == 15

# The input is taken from: https://adventofcode.com/2022/day/2/input
task_input = list(load_input_file('input.02.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
