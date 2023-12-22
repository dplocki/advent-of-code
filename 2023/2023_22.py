from typing import Dict, Generator, Iterable, Tuple


X, Y, Z, SIZE_X, SIZE_Y, SIZE_Z = 0, 1, 2, 3, 4, 5


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[Tuple[int, int, int], Tuple[int, int, int]], None, None]:
    for line in task_input:
        tokens = line.split('~')

        yield tuple(map(lambda s: tuple(map(int, s.split(','))), tokens))


def is_intersection(rectangle_a_x: int, rectangle_a_y: int, rectangle_a_size_x: int, rectangle_a_size_y: int,
                    rectangle_b_x: int, rectangle_b_y: int, rectangle_b_size_x: int, rectangle_b_size_y: int):

    return not(
            rectangle_a_x + rectangle_a_size_x <= rectangle_b_x
            or rectangle_b_x + rectangle_b_size_x <= rectangle_a_x
            or rectangle_a_y + rectangle_a_size_y <= rectangle_b_y
            or rectangle_b_y + rectangle_b_size_y <= rectangle_a_y
        )


def are_bricks_intersected_in_z_axis(first_brick: Tuple[int, int, int, int, int, int], second_brick: Tuple[int, int, int, int, int, int]) -> bool:
    return is_intersection(
            first_brick[X], first_brick[Y], first_brick[SIZE_X], first_brick[SIZE_Y],
            second_brick[X], second_brick[Y], second_brick[SIZE_X], second_brick[SIZE_Y])


def clean_bricks(brick_data: Tuple[Tuple[int, int, int], Tuple[int, int, int]]) -> Tuple[int, ...]:
    a, b = brick_data

    return (
        min(a[X], b[X]),
        min(a[Y], b[Y]),
        min(a[Z], b[Z]),
        abs(a[X] - b[X]) + 1,
        abs(a[Y] - b[Y]) + 1,
        abs(a[Z] - b[Z]) + 1
    )


def is_the_only_support(brick_supported_by: Dict[int, set], index: int) -> bool:
    for i in brick_supported_by:
        if index == i:
            continue

        if index not in brick_supported_by[i]:
            continue

        if len(brick_supported_by[i]) > 1:
            continue
        else:
            return True

    return False


def sort_function(index_with_clean_brick: Tuple[int, Tuple[int, ...]]) -> int:
    return index_with_clean_brick[1][Z]


def simulate_felling_down(bricks: Iterable[Tuple[int, int, int, int, int, int, int]]) -> Generator[Tuple[int, int, int, int, int, int, int], None, None]:
    laying_bricks = []

    while bricks:
        incoming_index, incoming_brick = bricks.pop()
        bottom_z = 0

        for _, current_brick in laying_bricks:
            if are_bricks_intersected_in_z_axis(incoming_brick, current_brick):
                bottom_z = max(current_brick[Z] + current_brick[SIZE_Z] - 1, bottom_z)

        laying_bricks.append((
            incoming_index,
            (incoming_brick[X], incoming_brick[Y], bottom_z + 1,
             incoming_brick[SIZE_X], incoming_brick[SIZE_Y], incoming_brick[SIZE_Z])
        ))

    return laying_bricks


def solution_for_first_part(task_input: Iterable[str]) -> int:
    sorted_bricks = [(index, clean_brick) for index, clean_brick in (sorted(enumerate(map(clean_bricks, parse(task_input))), key=sort_function, reverse=True))]
    bricks = simulate_felling_down(sorted_bricks)

    brick_supported_by = {}
    for current_index, current_brick in bricks:
        brick_supported_by[current_index] = [index for index, brick in bricks if brick[Z] + brick[SIZE_Z] == current_brick[Z] and are_bricks_intersected_in_z_axis(current_brick, brick)]

    return sum(1 for index in brick_supported_by if not is_the_only_support(brick_supported_by, index))


example_input = '''1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9'''.splitlines()

assert solution_for_first_part(example_input) == 5

# The input is taken from: https://adventofcode.com/2023/day/22/input
task_input = list(load_input_file('input.22.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def count_supported_by(brick_supported_by: Dict[int, set], index: int) -> int:
    falling = set([index])
    previous = 0

    while previous != len(falling):
        previous = len(falling)

        for i in brick_supported_by:
            if not brick_supported_by[i]:
                continue

            if len(brick_supported_by[i] - falling) == 0:
                falling.add(i)

    return len(falling) - 1


def solution_for_second_part(task_input: Iterable[str]) -> int:
    sorted_bricks = [(index, clean_brick) for index, clean_brick in (sorted(enumerate(map(clean_bricks, parse(task_input))), key=sort_function, reverse=True))]
    bricks = simulate_felling_down(sorted_bricks)

    brick_supported_by = {}
    for current_index, current_brick in bricks:
        brick_supported_by[current_index] = set(index for index, brick in bricks if brick[Z] + brick[SIZE_Z] == current_brick[Z] and are_bricks_intersected_in_z_axis(current_brick, brick))

    return sum(count_supported_by(brick_supported_by, index) for index in brick_supported_by if is_the_only_support(brick_supported_by, index))


assert solution_for_second_part(example_input) == 7
print("Solution for the second part:", solution_for_second_part(task_input))