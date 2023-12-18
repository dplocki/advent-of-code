from typing import Generator, Iterable, Set, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[str, int, str], None, None]:
    for line in task_input:
        tokens = line.split(' ')
        yield tokens[0], int(tokens[1]), tokens[2]


def find_all_internal(digger_map: Set[Tuple[int, int]], start: Tuple[int, int]) -> Set[Tuple[int, int]]:
    to_check = [start]

    while to_check:
        current_point = to_check.pop()

        if current_point in digger_map:
            continue

        digger_map.add(current_point)

        for direction in ((0, -1), (1, 0), (-1, 0), (0, 1)):
            to_check.append((current_point[0] + direction[0], current_point[1] + direction[1]))

    return digger_map


def solution_for_first_part(task_input: Iterable[str]) -> int:
    dig_plan = list(parse(task_input))

    digger_map = set()
    point = 0,0

    for where, how_long, _ in dig_plan:
        if where == 'R':
            direction = 0, 1
        elif where == 'L':
            direction = 0, -1
        elif where == 'D':
            direction = 1, 0
        elif where == 'U':
            direction = -1, 0

        for i in range(how_long):
            point = point[0] + direction[0], point[1] + direction[1]
            digger_map.add(point)

    digger_map = find_all_internal(digger_map, (1,1))

    return len(digger_map)


example_input = '''R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)'''.splitlines()

assert solution_for_first_part(example_input) == 62

# The input is taken from: https://adventofcode.com/2023/day/18/input
task_input = list(load_input_file('input.18.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
