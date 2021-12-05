from collections import defaultdict
from typing import List
import re


def load_input_file(file_name: str) -> List[str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: List[str]):
    pattern = re.compile(r'(\d+),(\d+) -> (\d+),(\d+)')

    for line in task_input:
        groups = pattern.fullmatch(line)
        if groups:
            yield int(groups[1]), int(groups[2]), int(groups[3]), int(groups[4])


def solution_for_first_part(task_input):
    points = defaultdict(int)

    for xs, ys, xe, ye in parse(task_input):
        if xs == xe:
            for i in range(min(ys, ye), max(ys, ye) + 1):
                points[xs, i] += 1
        elif ys == ye:
            for i in range(min(xs, xe), max(xs, xe) + 1):
                points[i, ys] += 1

    return sum(1 for v in points.values() if v >= 2)


example_input = '''0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
'''.splitlines()

assert solution_for_first_part(example_input) == 5

# The input is taken from: https://adventofcode.com/2021/day/5/input
task_input = list(load_input_file('input.05.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
