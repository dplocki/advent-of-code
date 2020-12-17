from itertools import product
from operator import itemgetter


def load_input_file(file_name: str) -> [str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(lines: [str]):
    yield from ((x, y, c)
            for y, line in enumerate(lines)
            for x, c in enumerate(line))


def simulator(active_cubes: set, dimention_number: int) -> int:

    def get_all_points(active_cubes: set) -> [tuple]:
        ranges = [
                range(min(map(itemgetter(i), active_cubes)) - 1, max(map(itemgetter(i), active_cubes)) + 2)
                for i in range(dimention_number)]


        yield from product(*ranges)


    def count_active_neighbors(current: set, point: tuple) -> int:
        result = 0
        for neighbor in product([-1, 0, 1], repeat=dimention_number):
            if any(neighbor) and tuple(map(sum, zip(neighbor, point))) in current:
                result += 1

        return result


    for _ in range(6):
        next_generation = set()

        for cube in get_all_points(active_cubes):
            cube_is_active = cube in active_cubes
            active_neighbors = count_active_neighbors(active_cubes, cube)
            if (cube_is_active and 2 <= active_neighbors <= 3) or (not cube_is_active and active_neighbors == 3):
                next_generation.add(cube)

        active_cubes = next_generation

    return len(active_cubes)


def solution_for_first_part(task_input: list) -> int:
    return simulator(set((x, y, 0) for x, y, c in parse(task_input) if c == '#'), 3)


example_input = '''.#.
..#
###'''.splitlines()

solution_for_first_part(example_input) == 12

# The input is taken from: https://adventofcode.com/2020/day/17/input
task_input = list(load_input_file('input.17.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: list) -> int:
    return simulator(set((x, y, 0, 0) for x, y, c in parse(task_input) if c == '#'), 4)


assert solution_for_second_part(example_input) == 848
print("Solution for the second part:", solution_for_second_part(task_input))
