from functools import reduce
from typing import Any, Generator, Iterable, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def get_value_of_letter(letter: str) -> int:
    if letter.islower():
        return ord(letter) - ord('a') + 1

    return ord(letter) - ord('A') + 27


def solution_for_first_part(input_lines: Iterable[str]) -> int:
    result = 0

    for line in input_lines:
        half_of_line = len(line) // 2
        first = set(line[:half_of_line])
        second = set(line[half_of_line:])
        repeating_letter = next(iter(first.intersection(second)))

        result += get_value_of_letter(repeating_letter)

    return result


example_input = '''vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
'''.splitlines()

assert solution_for_first_part(example_input) == 157

# The input is taken from: https://adventofcode.com/2022/day/3/input
task_input = list(load_input_file('input.03.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def split_by(lines: Iterable[Any], n: int) -> Iterable[Tuple[Any, ...]]:
    group = []
    for line in lines:
        group.append(line)
        if len(group) == n:
            yield tuple(group)
            group = []

    assert not group


def solution_for_second_part(input_lines: Iterable[str]) -> int:
    result = 0

    for lines in split_by(input_lines, 3):
        repeating_letter = next(iter(reduce(lambda a, b: a & b, map(set, lines))))
        result += get_value_of_letter(repeating_letter)

    return result


assert solution_for_second_part(example_input) == 70

print("Solution for the second part:", solution_for_second_part(task_input))
