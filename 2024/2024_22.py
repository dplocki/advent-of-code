from typing import Generator, Iterable
from more_itertools import last
import collections
import itertools


def sliding_window(iterable, n):
    """Collect data into overlapping fixed-length chunks or blocks.
    My current version of the more_itertools doesn't provide that
    Taken from: https://docs.python.org/3/library/itertools.html"""
    # sliding_window('ABCDEFG', 4) → ABCD BCDE CDEF DEFG
    iterator = iter(iterable)
    window = collections.deque(itertools.islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


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


def generate_secret(secret: int) -> Generator[int, None, None]:
    for _ in range(2000):
        secret = prune(mix(secret, secret * 64))
        secret = prune(mix(secret, secret // 32))
        secret = prune(mix(secret, secret * 2048))
        yield secret


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return sum(
        last(generate_secret(secret))
        for secret in parse(task_input))


assert mix(42, 15) == 37
assert prune(100000000) == 16113920

assert solution_for_first_part('''1
10
100
2024'''.splitlines()) == 37327623

# The input is taken from: https://adventofcode.com/2024/day/22/input
task_input = list(load_input_file('input.22.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def generate_price_difference(secret: int) -> Generator[int, None, None]:
    previous_price = 0

    for secret in generate_secret(secret):
        bananas = secret % 10
        yield bananas - previous_price, bananas
        previous_price = bananas


def solution_for_second_part(task_input: Iterable[str]) -> int:
    result = {}

    for secret in parse(task_input):
        sequence_values = {}
        for sequence in sliding_window(generate_price_difference(secret), 4):
            change = ','.join(str(s[0]) for s in sequence)
            if change not in sequence_values:
                sequence_values[','.join(str(s[0]) for s in sequence)] = sequence[-1][1]

        for k, v in sequence_values.items():
            result[k] = result.get(k, 0) + v

    return max(result.values())


assert solution_for_second_part('''1
2
3
2024'''.splitlines()) == 23

print("Solution for the second part:", solution_for_second_part(task_input))
