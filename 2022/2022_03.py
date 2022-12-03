from typing import Generator, Iterable


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def solution_for_first_part(input_lines: Iterable[str]) -> int:
    result = 0

    for line in input_lines:
        half_of_line = len(line) // 2
        first = set(line[:half_of_line])
        second = set(line[half_of_line:])

        repeating_letter = list(first.intersection(second))[0]

        if repeating_letter.islower():
            result += ord(repeating_letter) - ord('a') + 1
        else:
            result += ord(repeating_letter) - ord('A') + 27

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
result = solution_for_first_part(task_input)
print("Solution for the first part:", result)
