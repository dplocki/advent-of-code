from typing import Generator, Iterable, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple, None, None]:
    for line in task_input:
        yield tuple(map(int, line))


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return sum(
        max(
            batteries[first] * 10 + batteries[second]
            for first in range(len(batteries))
            for second in range(first + 1, len(batteries))
        )
        for batteries in parse(task_input)
    )


example_input = '''987654321111111
811111111111119
234234234234278
818181911112111'''.splitlines()

assert solution_for_first_part(example_input) == 357

# The input is taken from: https://adventofcode.com/2025/day/3/input
task_input = list(load_input_file('input.03.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
