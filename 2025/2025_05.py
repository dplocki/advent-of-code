from typing import Iterable, List, Tuple


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def parse(task_input: Iterable[str]) -> Tuple[List[Tuple[int, int]], List[int]]:
    raw_ranges, raw_ingredient = task_input.split('\n\n')

    return (
        [tuple(map(int, row.split('-'))) for row in raw_ranges.splitlines()],
        list(map(int, raw_ingredient.splitlines()))
    )


def solution_for_first_part(task_input: Tuple[List[Tuple[int, int]], List[int]]) -> int:
    ranges, ingredients = parse(task_input)

    return sum(1
        for ingredientID in ingredients
        if any(start <= ingredientID <= finish for start, finish in ranges))


example_input = '''3-5
10-14
16-20
12-18

1
5
8
11
17
32'''

assert solution_for_first_part(example_input) == 3
# The input is taken from: https://adventofcode.com/2025/day/5/input
task_input = load_input_file('input.05.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
