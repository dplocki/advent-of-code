from typing import List, Tuple


def load_input_file(file_name: str) -> List[str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: List[str]) -> List[Tuple[str, int]]:
    for line in task_input:
        tokens = line.split()
        yield tokens[0], int(tokens[1])


def solution_for_first_part(instructions: List[Tuple[str, int]]) -> int:
    depth = 0
    horizontal = 0

    for where, howMuch in instructions:
        if where == 'forward':
            horizontal += howMuch
        if where == 'down':
            depth += howMuch
        if where == 'up':
            depth -= howMuch

    return depth * horizontal


example_input = list(parse('''forward 5
down 5
forward 8
up 3
down 8
forward 2'''.splitlines()))

assert solution_for_first_part(example_input) == 150

# The input is taken from: https://adventofcode.com/2021/day/2/input
task_input = list(parse(load_input_file('input.02.txt')))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(instructions: List[Tuple[str, int]]) -> int:
    depth = 0
    aim = 0
    horizontal = 0

    for where, howMuch in instructions:
        if where == 'forward':
            horizontal += howMuch
            depth += aim * howMuch
        if where == 'down':
            aim += howMuch
        if where == 'up':
            aim -= howMuch

    return depth * horizontal


assert solution_for_second_part(example_input) == 900
print("Solution for the second part:", solution_for_second_part(task_input))
