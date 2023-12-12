from functools import cache
from typing import Generator, Iterable, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[str, Tuple[int, ...]], None, None]:
    for line in task_input:
        tokens = line.split(' ')

        yield tokens[0], tuple(map(int, tokens[1].split(',')))


@cache
def count_arrangements(line: str, numbers: Tuple[int, ...]) -> int:
    if len(numbers) == 0:
        return 0 if '#' in line else 1

    if line == '':
        return 0 if len(numbers) > 0 else 1

    result = 0
    first_group_size = numbers[0]
    for index in range(len(line)):
        if index + first_group_size > len(line):
            continue

        if '.' not in line[index:index + first_group_size] \
            and (index == 0 or line[index - 1] != '#') \
            and (index + first_group_size == len(line) or line[index + first_group_size] != '#'):
            result += count_arrangements(line[index + first_group_size + 1:], numbers[1:])

        if line[index] == '#':
            break

    return result


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return sum(
        count_arrangements(row, groups)
        for row, groups in parse(task_input))


example_input = '''???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1'''.splitlines()

assert solution_for_first_part(example_input) == 21

# The input is taken from: https://adventofcode.com/2023/day/12/input
task_input = list(load_input_file('input.12.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> int:
    return sum(
        count_arrangements('?'.join( (row,) * 5), groups * 5)
        for row, groups in parse(task_input))


assert solution_for_second_part(example_input) == 525152
print("Solution for the first part:", solution_for_second_part(task_input))
