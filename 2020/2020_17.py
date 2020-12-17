from operator import itemgetter


def load_input_file(file_name: str) -> [str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(lines: [str]):
    yield from ((x, y, c)
            for y, line in enumerate(lines)
            for x, c in enumerate(line))


def solution_for_first_part(task_input):

    def get_all_points(current: set) -> [tuple]:
        min_x = min(map(itemgetter(0), current)) - 1
        min_y = min(map(itemgetter(1), current)) - 1
        min_z = min(map(itemgetter(2), current)) - 1

        max_x = max(map(itemgetter(0), current)) + 2
        max_y = max(map(itemgetter(1), current)) + 2
        max_z = max(map(itemgetter(2), current)) + 2

        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                for z in range(min_z, max_z):
                    yield (x, y, z)


    def count_active_neighbors(current: set, point: tuple) -> int:
        result = 0
        neighbors = [-1, 0, 1]

        for x in neighbors:
            for y in neighbors:
                for z in neighbors:
                    if x == 0 and y == 0 and z == 0:
                        continue

                    if (x + point[0], y + point[1], z + point[2]) in current:
                        result += 1

        return result


    active_cubes = set((x, y, 0) for x, y, c in parse(task_input) if c == '#')

    for _ in range(6):
        next_generation = set()

        for cube in get_all_points(active_cubes):
            cube_is_active = cube in active_cubes
            active_neighbors = count_active_neighbors(active_cubes, cube)
            if (cube_is_active and 2 <= active_neighbors <= 3) or (not cube_is_active and active_neighbors == 3):
                next_generation.add(cube)

        active_cubes = next_generation

    return len(active_cubes)


example_input = '''.#.
..#
###'''.splitlines()

solution_for_first_part(example_input) == 12

# The input is taken from: https://adventofcode.com/2020/day/17/input
task_input = list(load_input_file('input.17.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
