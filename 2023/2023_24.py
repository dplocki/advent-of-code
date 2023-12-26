from typing import Generator, Iterable, Tuple
import itertools


X, Y, Z, DELTA_X, DELTA_Y, DELTA_Z = range(6)
A, B, C = 0, 1, 2


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[int, int, int, int, int, int], None, None]:
    for line in task_input:
        yield tuple(map(int, line.replace(' @ ', ', ').split(',')))


def transform_to_linear_equation(hailstone: Tuple[int, int, int, int, int, int]) -> Tuple[int, int, int]:
    return hailstone[DELTA_Y], - hailstone[DELTA_X], hailstone[X] * hailstone[DELTA_Y] - hailstone[Y] * hailstone[DELTA_X]


def find_intersection_in_area(task_input: Iterable[str], minimum: int, maximum: int) -> int:
    result = 0

    for hailstone_a, hailstone_b in itertools.combinations(parse(task_input), 2):
        hailstone_path_1 = transform_to_linear_equation(hailstone_a)
        hailstone_path_2 = transform_to_linear_equation(hailstone_b)

        if hailstone_path_1[A] * hailstone_path_2[B] == hailstone_path_2[A] * hailstone_path_1[B]:
            continue

        x = (hailstone_path_1[C] * hailstone_path_2[B] - hailstone_path_1[B] * hailstone_path_2[C]) / (hailstone_path_1[A] * hailstone_path_2[B] - hailstone_path_2[A] * hailstone_path_1[B])
        y = (hailstone_path_1[C] * hailstone_path_2[A] - hailstone_path_1[A] * hailstone_path_2[C]) / (hailstone_path_2[A] * hailstone_path_1[B] - hailstone_path_2[B] * hailstone_path_1[A])

        t_a = (x - hailstone_a[X]) / hailstone_a[DELTA_X]
        t_b = (x - hailstone_b[X]) / hailstone_b[DELTA_X]

        if t_a < 0 or t_b < 0:
            continue

        if minimum <= x <= maximum and minimum <= y <= maximum:
            result += 1

    return result


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return find_intersection_in_area(task_input, 200000000000000, 400000000000000)


example_input = '''19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3'''.splitlines()

assert find_intersection_in_area(example_input, 7, 27) == 2

# The input is taken from: https://adventofcode.com/2023/day/24/input
task_input = list(load_input_file('input.24.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
