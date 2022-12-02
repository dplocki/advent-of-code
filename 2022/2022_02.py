from typing import Callable, Generator, Iterable, List, Tuple
from enum import Enum


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


WINNING_TABLE = {
    Shape.ROCK: Shape.PAPER,
    Shape.PAPER: Shape.SCISSORS,
    Shape.SCISSORS: Shape.ROCK
}


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: List[str]) -> Generator[Tuple[str, str], None, None]:
    for line in task_input:
        yield line.split(' ')


def result_of_match(opponent: Shape, me: Shape) -> int:
    if opponent == me:
        return 3

    if WINNING_TABLE[opponent] == me:
        return 6

    return 0


def solution(task_input: Iterable[str], calculate_mine_response_function: Callable[[Shape, str], Shape]) -> int:
    lines = parse(task_input)

    opponent_convert_table = {
        'A': Shape.ROCK,
        'B': Shape.PAPER,
        'C': Shape.SCISSORS
    }

    result = 0
    for opponent, me in lines:
        opponent_choice = opponent_convert_table[opponent]
        mine_choice = calculate_mine_response_function(opponent_choice, me)
        result += mine_choice.value + result_of_match(opponent_choice, mine_choice)

    return result


def solution_for_first_part(task_input: Iterable[str]) -> int:

    mine_convert_table = {
        'X': Shape.ROCK,
        'Y': Shape.PAPER,
        'Z': Shape.SCISSORS
    }

    return solution(task_input, lambda _, response: mine_convert_table[response])


example_input = '''A Y
B X
C Z'''.splitlines()

assert solution_for_first_part(example_input) == 15

# The input is taken from: https://adventofcode.com/2022/day/2/input
task_input = list(load_input_file('input.02.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> int:

    REVERSED_WINNING_TABLE = {v:k for k, v in WINNING_TABLE.items()}

    def internal(opponent_choice, response):
        if response == 'X':
            return REVERSED_WINNING_TABLE[opponent_choice]
        elif response == 'Y':
            return opponent_choice
        
        return WINNING_TABLE[opponent_choice]

    return solution(task_input, internal)


assert solution_for_second_part(example_input) == 12

print("Solution for the second part:", solution_for_second_part(task_input))
