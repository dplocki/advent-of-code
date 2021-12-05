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


def mark_lines(points_map, points):
    xs, ys, xe, ye = points

    if xs == xe:
        for i in range(min(ys, ye), max(ys, ye) + 1):
            points_map[xs, i] += 1
    elif ys == ye:
        for i in range(min(xs, xe), max(xs, xe) + 1):
            points_map[i, ys] += 1

    return points_map


def find_overlapping(task_input, mark_points):
    point_map = defaultdict(int)

    for points in parse(task_input):
        point_map = mark_points(point_map, points)

    return sum(1 for v in point_map.values() if v >= 2)


def solution_for_first_part(task_input):
    return find_overlapping(task_input, mark_lines)


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


def solution_for_second_part(task_input):

    def mark_digals(points_map, points):
        xs, ys, xe, ye = points

        if abs(xs - xe) == abs(ys - ye):
            nxs, nxe = min(xs, xe), max(xs, xe)
            nys, nye = (ys, ye) if nxs == xs else (ye, ys)

            step = 1 if nys < nye else -1

            for i in range(0, nxe - nxs + 1):
                points_map[nxs + i, nys + step * i] += 1

        return points_map

    def mark_with_digals(points_map, points):
        points_map = mark_digals(points_map, points)
        return mark_lines(points_map, points)


    return find_overlapping(task_input, mark_with_digals)


assert solution_for_second_part(example_input) == 12
print("Solution for the second part:", solution_for_second_part(task_input))
