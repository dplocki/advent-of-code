import re
from typing import Generator, Iterator, List, Tuple


def load_input_file(file_name: str) -> List[str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: List[str]) -> Generator[Tuple[int, int, int, int], None, None]:
    NUMBERS_TO_PARSE = 4

    pattern = re.compile(r'(\d+)-(\d+),(\d+)-(\d+)')
    for line in task_input:
        groups = pattern.match(line)
        yield tuple(map(int, (groups[g + 1] for g in range(NUMBERS_TO_PARSE))))


def solution_for_first_part(task_input: Iterator[str]) -> int:
    lines = parse(task_input)

    result = 0
    for elf_1_start, elf_1_end, elf_2_start, elf_2_end in lines:
        first_elf_range = set(range(elf_1_start, elf_1_end + 1)) 
        second_elf_range = set(range(elf_2_start, elf_2_end + 1))

        if first_elf_range <= second_elf_range or second_elf_range <= first_elf_range:
            result += 1

    return result


example_input = '''2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8'''.splitlines()

assert solution_for_first_part(example_input) == 2

# The input is taken from: https://adventofcode.com/2022/day/4/input
task_input = list(load_input_file('input.04.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
