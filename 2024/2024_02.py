from typing import Generator, Iterable
import itertools


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]):
    for line in task_input:
        yield list(map(int, line.split()))


def is_safe(report: Iterable[int]) -> bool:
    is_increasing = report[0] > report[1]

    for a, b in itertools.pairwise(report):

        if a == b:
            return False

        if is_increasing and a < b:
            return False

        if not is_increasing and a > b:
            return False


        difference = abs(a - b)

        if difference < 1 or difference > 3:
            return False

    return True


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return sum(1 if is_safe(report) else 0
        for report in parse(task_input)
    )


example_input = '''7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9'''.splitlines()

solution_for_first_part(example_input) == 2

# The input is taken from: https://adventofcode.com/2024/day/2/input
task_input = list(load_input_file('input.02.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def is_dampener_safe(report: Iterable[int]) -> bool:
    for index in range(len(report)):
        if is_safe(report):
            return True

        if is_safe(report[:index] + report[index + 1:]):
            return True

    return False


def solution_for_second_part(task_input: Iterable[str]) -> int:
    return sum(1 if is_dampener_safe(report) else 0
        for report in parse(task_input)
    )


print("Solution for the second part:", solution_for_second_part(task_input))
