from typing import List


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def parse(task_input: str) -> List[List[int]]:
    return (
            [int(line) for line in group.splitlines()]
            for group in task_input.split('\n\n')
        )


def solution_for_first_part(task_input: str) -> int:
    elf_lists = parse(task_input)

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

assert solution_for_first_part(example_input) == 24000

# The input is taken from: https://adventofcode.com/2022/day/1/input
task_input = load_input_file('input.01.txt')
result = solution_for_first_part(task_input)
print("Solution for the first part:", result)
