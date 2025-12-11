from typing import Generator, Iterable, Tuple
from functools import reduce
from collections import deque
import operator


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[str, Tuple[Tuple[int, ...], ...], Tuple[int, ...]], None, None]:
    for line in task_input:
        tokens = line.split(' ')

        indicator_lights = tokens[0][1:-1]
        buttons_sets = tuple(map(lambda x: tuple(map(int, x.split(','))), map(lambda x: x[1:-1], tokens[1:-1])))
        joltage = tuple(map(int, tokens[-1][1:-1].split(',')))

        yield indicator_lights, buttons_sets, joltage


def find_button_number(indicator_lights, buttons_sets):
    buttons_imprints = [
        reduce(operator.or_, (1 << button for button in buttons_set), 0)
        for buttons_set in buttons_sets
    ]

    required = int(indicator_lights[::-1].replace('.', '0').replace('#', '1'), 2)
    visited = set()
    queue = deque([(0, 0)])

    while queue:
        current, button_pressed = queue.popleft()
        if current in visited:
            continue

        if current == required:
            return button_pressed

        visited.add(current)
        new_button_pressed = button_pressed + 1
        for buttons_imprint in buttons_imprints:
            queue.append((current ^ buttons_imprint, new_button_pressed))

    raise Exception('Unexpected: cannot find the answer')


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return sum(
        find_button_number(indicator_lights, buttons_sets)
        for indicator_lights, buttons_sets, _ in parse(task_input))


example_input = '''[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}'''.splitlines()

assert solution_for_first_part(example_input) == 7

# The input is taken from: https://adventofcode.com/2025/day/10/input
task_input = list(load_input_file('input.10.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
