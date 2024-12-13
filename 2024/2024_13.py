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


def find_all_match(button_a_x: int, button_a_y: int, button_b_x: int, button_b_y: int, target_x: int, target_y: int) -> int:
    b = (target_x * button_a_y - target_y * button_a_x) // (button_a_y * button_b_x - button_b_y * button_a_x)
    a = (target_x * button_b_y - target_y * button_b_x) // (button_b_y * button_a_x - button_b_x * button_a_y)

    if (a * button_a_x + b * button_b_x == target_x) and (a * button_a_y + b * button_b_y == target_y):
        return a * 3 + b

    return 0


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return sum(
        find_all_match(*parameters)
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


def solution_for_second_part(task_input: Iterable[str]) -> int:
    return sum(
        find_all_match(button_a_x, button_a_y, button_b_x, button_b_y, price_x + 10_000_000_000_000, price_y + 10_000_000_000_000)
        for button_a_x, button_a_y, button_b_x, button_b_y, price_x, price_y in parse(task_input))


print("Solution for the second part:", solution_for_second_part(task_input))
