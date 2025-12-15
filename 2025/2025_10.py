from itertools import chain, combinations
import sys
from typing import Generator, Iterable, Tuple
from functools import cache, reduce
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


def find_the_lowest_buttons_press_count(goal: int, buttons_sets: Tuple[int, ...]) -> Tuple[int, ...]:
    visited = set()
    queue = deque([(0, tuple([0] * len(buttons_sets)))])

    while queue:
        current, buttons_pressed = queue.popleft()
        if current in visited:
            continue

        if current == goal:
            return buttons_pressed

        visited.add(current)
        button_pressed_list = list(buttons_pressed)
        for index, buttons_set in enumerate(buttons_sets):
            button_pressed_list[index] += 1
            queue.append((current ^ buttons_set, tuple(button_pressed_list)))
            button_pressed_list[index] -= 1

    raise Exception('Unexpected: unable to find the answer')


def solution_for_first_part(task_input: Iterable[str]) -> int:

    def transformation(indicator_lights: str, buttons_imprints: Tuple[Tuple[int, ...], ...]) -> int:
        buttons_sets = [
            reduce(operator.or_, (1 << button for button in buttons_set), 0)
            for buttons_set in buttons_imprints
        ]

        goal = int(indicator_lights[::-1].replace('.', '0').replace('#', '1'), 2)

        return find_the_lowest_buttons_press_count(goal, buttons_sets)


    return sum(
        sum(transformation(indicator_lights, buttons_sets))
        for indicator_lights, buttons_sets, _ in parse(task_input))


example_input = '''[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}'''.splitlines()

assert solution_for_first_part(example_input) == 7

# The input is taken from: https://adventofcode.com/2025/day/10/input
task_input = list(load_input_file('input.10.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> int:


    def transformation(buttons_imprints: Tuple[Tuple[int, ...]], joltage: Tuple[int, ...]) -> int:

        @cache
        def internal(required: Tuple[int]):
            if all(r == 0 for r in required):
                return 0

            result = sys.maxsize
            for changes, press_count in press_button_list.items():
                if not all(r >= c and c % 2 == r % 2 for c, r in zip(changes, required)):
                    continue

                new_required = list(required)
                for index, change in enumerate(changes):
                    new_required[index] -= change

                result = min(result, 2 * internal(tuple(r // 2 for r in new_required)) + press_count)

            return result

        press_button_list = {}
        for subset in chain.from_iterable(combinations(buttons_imprints, subset_length) for subset_length in range(len(buttons_imprints) + 1)):
            key_as_list = [0] * len(joltage)
            for s in chain.from_iterable(subset):
                key_as_list[s] += 1

            key_as_tuple = tuple(key_as_list)
            if key_as_tuple not in press_button_list:
                press_button_list[key_as_tuple] = len(subset)

        return internal(tuple(joltage))


    return sum(
        transformation(buttons_imprints, joltage)
        for _, buttons_imprints, joltage in parse(task_input))


assert solution_for_second_part(example_input) == 33
print("Solution for the second part:", solution_for_second_part(task_input))
