from typing import List


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def parse(task_input: str) -> List[List[int]]:
    return (
            [int(line) for line in group.splitlines()]
            for group in task_input.split('\n\n')
        )


def solution_for_first_part(elf_lists: List[List[str]]) -> int:
    return max(
        sum(food for food in elf_list)
        for elf_list in elf_lists
    )


example_input = '''1000
2000
3000

4000

5000
6000

7000
8000
9000

10000'''

assert solution_for_first_part(parse(example_input)) == 24000

# The input is taken from: https://adventofcode.com/2022/day/1/input
task_input = list(parse(load_input_file('input.01.txt')))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(elf_lists: List[List[str]]) -> int:
    sorted_elf_calories = sorted(sum(elf_list) for elf_list in elf_lists)

    return sum(sorted_elf_calories[-3:])


assert solution_for_second_part(parse(example_input)) == 45000
print("Solution for the second part:", solution_for_second_part(task_input))

