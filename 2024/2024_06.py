from typing import Generator, Iterable, Set, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Tuple[Set[Tuple[int, int]], Tuple[int, int], Tuple[int, int]]:
    rows = 0
    level_map = set()
    start_point = None

    for row, line in enumerate(task_input):
        columns = len(task_input[0])
        rows += 1

        for column, character in enumerate(line):
            if character == '#':
                level_map.add((row, column))
            elif character == '^':
                start_point = (row, column)

    return level_map, (rows, columns), start_point


def is_outside_map(size: Tuple[int, int], row: int, column: int) -> bool:
    if row < 0 or row >= size[0]:
        return True

    if column < 0 or column >= size[1]:
        return True

    return False


def solution_for_first_part(task_input: Iterable[str]) -> int:
    level_map, size, start_point = parse(task_input)
    row, column = start_point
    direction = 0
    visited = set()

    while True:
        if is_outside_map(size, row, column):
            return len(visited)

        visited.add((row, column))

        if direction == 0 and (row - 1, column) not in level_map:
            row -= 1
        elif direction == 1 and (row, column + 1) not in level_map:
            column += 1
        elif direction == 2 and (row + 1, column) not in level_map:
            row += 1
        elif direction == 3 and (row, column - 1) not in level_map:
            column -= 1
        else:
            direction = (direction + 1) % 4


example_input = '''....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...'''.splitlines()

assert solution_for_first_part(example_input) == 41

# The input is taken from: https://adventofcode.com/2024/day/6/input
task_input = list(load_input_file('input.06.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))

