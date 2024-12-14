from typing import Generator, Iterable, Tuple
import re


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[int, int, int, int], None, None]:
    PATTERN = r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)"
    for line in task_input:
        for group in re.findall(PATTERN, line):
            yield tuple(map(int, group))


def solution_for_first_part(task_input: Iterable[str], wide, tall) -> int:
    robots = {value for value in parse(task_input)}

    for _ in range(100):
        robots = (
            ((position_x + speed_x) % wide, (position_y + speed_y) % tall, speed_x, speed_y)
            for position_x, position_y, speed_x, speed_y in robots)

    positions = [(x, y) for x, y, _, _ in robots]

    first_quatre = sum(1 for x, y in positions if x < wide // 2 and y < tall // 2)
    second_quatre = sum(1 for x, y in positions if x > wide // 2 and y < tall // 2)
    third_quatre = sum(1 for x, y in positions if x < wide // 2 and y > tall // 2)
    fourth_quatre = sum(1 for x, y in positions if x > wide // 2 and y > tall // 2)

    return first_quatre * second_quatre * third_quatre * fourth_quatre


example_input = '''p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3'''.splitlines()

assert solution_for_first_part(example_input, 11, 7) == 12

# The input is taken from: https://adventofcode.com/2024/day/14/input
task_input = list(load_input_file('input.14.txt'))
print("Solution for the first part:", solution_for_first_part(task_input, 101, 103))
