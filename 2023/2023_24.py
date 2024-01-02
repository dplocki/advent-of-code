from typing import Generator, Iterable, Tuple
import itertools


X, Y, Z, DELTA_X, DELTA_Y, DELTA_Z = range(6)


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[int, int, int, int, int, int], None, None]:
    for line in task_input:
        yield tuple(map(int, line.replace(' @ ', ', ').split(',')))


def intersection(hailstone_a: Tuple[int, int, int, int, int, int], hailstone_b: Tuple[int, int, int, int, int, int]) -> Tuple[int, int]:
    determinant = hailstone_a[DELTA_X] * hailstone_b[DELTA_Y] - hailstone_a[DELTA_Y] * hailstone_b[DELTA_X]
    if determinant == 0:
        return None

    b_a = hailstone_a[DELTA_X] * hailstone_a[Y] - hailstone_a[DELTA_Y] * hailstone_a[X]
    b_b = hailstone_b[DELTA_X] * hailstone_b[Y] - hailstone_b[DELTA_Y] * hailstone_b[X]

    return (
        (hailstone_b[DELTA_X] * b_a - hailstone_a[DELTA_X] * b_b) / determinant,
        (hailstone_b[DELTA_Y] * b_a - hailstone_a[DELTA_Y] * b_b) / determinant
    )


def find_intersection_in_area(task_input: Iterable[str], minimum: int, maximum: int) -> int:
    result = 0

    for hailstone_a, hailstone_b in itertools.combinations(parse(task_input), 2):
        intersection_point = intersection(hailstone_a, hailstone_b)
        if intersection_point == None:
            continue

        x, y = intersection_point
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


def find_location_of_stone_in_2d(hailstones: Iterable[Tuple[int, int, int, int, int, int]]) -> Tuple[int, int]:
    min_speed_delta_range = -300
    max_speed_delta_range = 300

    for delta_x in range(min_speed_delta_range, max_speed_delta_range):
        for delta_y in range(min_speed_delta_range, max_speed_delta_range):
            new_hailstones = [
                (hailstone[X], hailstone[Y], None, hailstone[DELTA_X] + delta_x, hailstone[DELTA_Y] + delta_y, None)
                for hailstone in hailstones
            ]

            potential_rock_location = intersection(new_hailstones[0], new_hailstones[1])
            if potential_rock_location == None:
                continue

            if all(
                    abs((potential_rock_location[0] - hailstone[X]) * hailstone[DELTA_Y] - (potential_rock_location[1] - hailstone[Y]) * hailstone[DELTA_X]) < 0.0001
                    for hailstone in new_hailstones
                ):

                return potential_rock_location

    raise Exception('Not found')


def solution_for_second_part(task_input: Iterable[str]) -> int:
    hailstones = list(parse(task_input))

    stone_location_xy = find_location_of_stone_in_2d([
        (hailstone[X], hailstone[Y], None, hailstone[DELTA_X], hailstone[DELTA_Y], None)
        for hailstone in hailstones
    ])
    stone_location_xz = find_location_of_stone_in_2d([
        (hailstone[X], hailstone[Z], None, hailstone[DELTA_X], hailstone[DELTA_Z], None)
        for hailstone in hailstones
    ])

    return int(stone_location_xy[0] + stone_location_xy[1] + stone_location_xz[1])


assert solution_for_second_part(example_input) == 47

print("Solution for the second part:", solution_for_second_part(task_input))
