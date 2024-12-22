from typing import Generator, Iterable


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[int, None, None]:
    for line in task_input:
        yield int(line)


def mix(secret: int, value: int) -> int:
    return secret ^ value


def prune(secret: int) -> int:
    return secret % 16777216


def solution_for_first_part(task_input: Iterable[str]) -> int:
    result = 0

    for secret in parse(task_input):
        for _ in range(2000):
            secret = prune(mix(secret, secret * 64))
            secret = prune(mix(secret, secret // 32))
            secret = prune(mix(secret, secret * 2048))

        result += secret

    return result


assert mix(42, 15) == 37
assert prune(100000000) == 16113920

assert solution_for_first_part('''1
10
100
2024'''.splitlines()) == 37327623

# The input is taken from: https://adventofcode.com/2024/day/22/input
task_input = list(load_input_file('input.22.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
