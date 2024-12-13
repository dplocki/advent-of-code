from typing import Generator, Iterable, Tuple
import re


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def parse(task_input: Iterable[str]) -> Generator[Tuple[int, int, int, int, int, int], None, None]:
    PATTERN = r"""Button A: X\+(\d+), Y\+(\d+)
Button B: X\+(\d+), Y\+(\d+)
Prize: X=(\d+), Y=(\d+)
"""

    yield from (
        tuple(map(int, group))
        for group in re.findall(PATTERN, task_input)
    )


def find_all_matches(button_a_x: int, button_a_y: int, button_b_x: int, button_b_y: int, target_x: int, target_y: int) -> int:
    MAX_STEP = 101

    for a in range(MAX_STEP):
        for b in range(MAX_STEP):
            reach_x = a * button_a_x + b * button_b_x
            reach_y = a * button_a_y + b * button_b_y
            price = a * 3 + b * 1

            if reach_x == target_x and reach_y == target_y:
                return price # apparently there is only one solution

    return 0


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return sum(
        find_all_matches(*parameters)
        for parameters in parse(task_input))


example_input = '''Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279'''

assert solution_for_first_part(example_input) == 480

# The input is taken from: https://adventofcode.com/2024/day/13/input
task_input = load_input_file('input.13.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
