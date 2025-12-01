from typing import Generator, Iterable, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[str, int], None, None]:
    for line in task_input:
        yield line[0], int(line[1:])


def solution_for_first_part(task_input: Iterable[str]) -> int:
    dial = 50
    result = 0

    for w, v in parse(task_input):
        if w == 'R':
            dial += v
        elif w == 'L':
            dial -= v

        dial = dial % 100

        if dial == 0:
            result += 1

    return result


example_input = '''L68
L30
R48
L5
R60
L55
L1
L99
R14
L82'''.splitlines()

assert solution_for_first_part(example_input) == 3

# The input is taken from: https://adventofcode.com/2025/day/1/input
task_input = list(load_input_file('input.01.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
