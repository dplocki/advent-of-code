from typing import Generator, Iterable


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> tuple[Iterable[int], Iterable[int]]:
    lefts = []
    rights = []

    for line in task_input:
        tokens = tuple(map(int, line.split()))
        lefts.append(tokens[0])
        rights.append(tokens[1])

    return lefts, rights


def solution_for_first_part(task_input: Iterable[str]) -> int:
    lefts, rights = parse(task_input)

    lefts.sort()
    rights.sort()

    return sum(abs(left - right) for left, right in zip(lefts, rights))


example_input = '''3   4
4   3
2   5
1   3
3   9
3   3
'''.splitlines()

assert solution_for_first_part(example_input) == 11

# The input is taken from: https://adventofcode.com/2024/day/1/input
task_input = list(load_input_file('input.01.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> int:
    lefts, rights = parse(task_input)

    return sum(
        left * rights.count(left)
        for left in lefts)


assert solution_for_second_part(example_input) == 31
print("Solution for the second part:", solution_for_second_part(task_input))
