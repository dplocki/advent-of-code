MAXIUM_HEIGHT = 9


def load_input_file(file_name: str) -> list[str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: list[str]) -> list[tuple[int, int, int]]:
    for row_number, line in enumerate(task_input):
        for column_number, digit in enumerate(line):
            yield row_number, column_number, int(digit)


def get_four_neighbors(x: int, y: int) -> tuple[int, int]:
    yield (x, y - 1) # NORTH
    yield (x + 1, y) # EAST
    yield (x, y + 1) # SOUTH
    yield (x - 1, y) # WEST


def find_lowest_points(height_map: dict[tuple[int, int], int]) -> list[int, int]:
    yield from (coordinate
        for coordinate, height in height_map.items()
        if all(map(lambda neighbore: height_map.get(neighbore, MAXIUM_HEIGHT) > height, get_four_neighbors(*coordinate))))


def build_height_map(task_input: list[tuple[int, int, int]]) -> dict[tuple[int, int], int]:
    return {(row, column):value for row, column, value in parse(task_input)}


def solution_for_first_part(height_map: dict[tuple[int, int], int]) -> int:
    return sum(height_map[coordinate] + 1 for coordinate in find_lowest_points(height_map))


example_input = '''2199943210
3987894921
9856789892
8767896789
9899965678'''.splitlines()

assert solution_for_first_part(build_height_map(example_input)) == 15

# The input is taken from: https://adventofcode.com/2021/day/9/input
task_input = build_height_map(load_input_file('input.09.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(height_map: dict[tuple[int, int], int]) -> int:


    def find_basin_size(height_map: dict[tuple[int, int], int], coordinate: tuple[int, int]) -> int:
        basin_points = set()
        points_to_check = [coordinate]

        while points_to_check:
            current_point = points_to_check.pop()
            basin_points.add(current_point)

            for neigbore in get_four_neighbors(*current_point):
                if neigbore not in basin_points and neigbore in height_map and height_map[neigbore] < MAXIUM_HEIGHT:
                    points_to_check.append(neigbore)

        return len(basin_points)


    basin_sizes = [find_basin_size(height_map, coordinate) for coordinate in find_lowest_points(height_map)]
    basin_sizes.sort(reverse=True)

    return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]


assert solution_for_second_part(build_height_map(example_input)) == 1134
print("Solution for the second part:", solution_for_second_part(task_input))
