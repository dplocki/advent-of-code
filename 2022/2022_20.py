from typing import Generator, Iterable, List, Tuple
from collections import deque


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[int, None, None]:
    for line in task_input:
        yield int(line)


def mix(original_list: List[Tuple[int, int]], current_list: deque) -> deque:
    for original_value in original_list:
        current_list.rotate(-current_list.index(original_value))

        current_list.popleft()
        current_list.rotate(-original_value[0])
        current_list.appendleft(original_value)


def solution_for_first_part(task_input: Iterable[str]) -> int:
    original_list = [(value, index) for index, value in enumerate(parse(task_input))]
    current_list = deque(original_list)

    mix(original_list, current_list)

    index_of_zero_element = current_list.index((0, next(k for v, k in original_list if v == 0)))

    return sum(
        current_list[(index - index_of_zero_element + 1) * 1000 % len(original_list)][0]
        for index in range(3))


example_input = '''1
2
-3
3
-2
0
4'''.splitlines()

assert solution_for_first_part(example_input) == 3

# The input is taken from: https://adventofcode.com/2022/day/20/input
task_input = list(load_input_file('input.20.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> int:
    original_list = [(v * 811589153, index) for index, v in enumerate(parse(task_input))]
    current_list = deque(original_list)

    for _ in range(10):
        mix(original_list, current_list)

    index_of_zero_element = current_list.index((0, next(k for v, k in original_list if v == 0)))

    return sum(
        current_list[(index - index_of_zero_element + 1) * 1000 % len(original_list)][0]
        for index in range(3))


assert solution_for_second_part(example_input) == 1623178306
print("Solution for the second part:", solution_for_second_part(task_input))
