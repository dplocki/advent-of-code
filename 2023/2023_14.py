from typing import Dict, Generator, Iterable, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Tuple[Dict[Tuple[int, int], str], int, int]:
    maximum_row = 0
    maximum_columns = 0

    rock_map = {}
    for row_index, line in enumerate(task_input):
        maximum_row += 1
        for column_index, character in enumerate(line):
            maximum_columns = len(line)
            if character in '#O':
                rock_map[row_index, column_index] = character

    return rock_map, maximum_row, maximum_columns


def find_balance(rock_map: Dict[Tuple[int, int], str], row_max: int, columns_max: int, start: Tuple[int, int], direction: Tuple[int, int]) -> Tuple[int, int]:
    strip = []
    point = start
    while (point[0] >= 0 and \
        point[1] >= 0 and \
        point[0] <= row_max -1  and \
        point[1] <= columns_max -1 and \
        rock_map.get(point, '.') != '#'):

        strip.append(rock_map.get(point, '.'))
        point = point[0] + direction[0], point[1] + direction[1]

    moving_rocks = 0
    for item in strip[1:]:
        if item == 'O':
            moving_rocks += 1
        elif item == '#':
            break

    strip_size = len(strip) - 1
    return (
            start[0] + (strip_size - moving_rocks) * direction[0],
            start[1] + (strip_size - moving_rocks) * direction[1]
        )


def count_total_load(rock_map: Dict[Tuple[int, int], str], maximum_row: int) -> int:
    return sum(
        maximum_row - position[0]
        for position, object in rock_map.items()
        if object == 'O')


def solution_for_first_part(task_input: Iterable[str]) -> int:
    rock_map, row_max, columns_max = parse(task_input)

    new_rock_map = {}
    for coord, value in rock_map.items():
        if value == 'O':
            new_rock_map[find_balance(rock_map, row_max, columns_max, coord, (-1, 0))] = 'O'
        elif value == '#':
            new_rock_map[coord] = '#'

    return count_total_load(new_rock_map, row_max)


example_input = '''O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....'''.splitlines()

assert solution_for_first_part(example_input) == 136

# The input is taken from: https://adventofcode.com/2023/day/14/input
task_input = list(load_input_file('input.14.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def cycle_rotation_of_dish(rock_map: Dict[Tuple[int, int], str], row_max: int, columns_max: int) -> Dict[Tuple[int, int], str]:
    for direction in ((-1, 0), (0, -1), (1, 0), (0, 1)):
        new_rock_map = {}
        for coord, value in rock_map.items():
            if value == 'O':
                new_rock_map[find_balance(rock_map, row_max, columns_max, coord, direction)] = 'O'
            elif value == '#':
                new_rock_map[coord] = '#'

        rock_map = new_rock_map

    return rock_map


def solution_for_second_part(task_input: Iterable[str]) -> int:
    rock_map, maximum_row, maximum_columns = parse(task_input)

    previous_rock_maps = []
    results = []

    for cycle_number in range(1_000_000_000):
        rock_map = cycle_rotation_of_dish(rock_map, maximum_row, maximum_columns)

        signature_of_rock_map = set(p for p, k in rock_map.items() if k == 'O')
        if signature_of_rock_map in previous_rock_maps:
            found_index = previous_rock_maps.index(signature_of_rock_map)
            return results[found_index + (1_000_000_000 - cycle_number - 1) % (cycle_number - found_index)]

        previous_rock_maps.append(signature_of_rock_map)
        results.append(count_total_load(rock_map, maximum_row))

    return count_total_load(rock_map, maximum_row)


assert solution_for_second_part(example_input) == 64
print("Solution for the second part:", solution_for_second_part(task_input))
