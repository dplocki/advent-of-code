from typing import Dict, Generator, Iterable, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Dict[Tuple[int, int], str]:
    return {
        (row_index, column_index): character
        for row_index, line in enumerate(task_input)
        for column_index, character in enumerate(line)
    }


def solution_for_first_part(task_input: Iterable[str]) -> int:
    mirrors_map = parse(task_input)
    visited = set()
    rays = [(0, 0, 0, 1)]

    while rays:
        row_index, column_index, row_delta, column_delta = rays.pop()

        if (row_index, column_index) not in mirrors_map:
            continue

        if (row_index, column_index, row_delta, column_delta) in visited:
            continue

        visited.add((row_index, column_index, row_delta, column_delta))

        element_on_coordinates = mirrors_map[row_index, column_index]
        if element_on_coordinates == '\\':
            if row_delta == 1 and column_delta == 0:
                row_delta, column_delta = 0, 1
            elif row_delta == -1 and column_delta == 0:
                row_delta, column_delta = 0, -1
            elif row_delta == 0 and column_delta == 1:
                row_delta, column_delta = 1, 0
            elif row_delta == 0 and column_delta == -1:
                row_delta, column_delta = -1, 0

        elif element_on_coordinates == '/':
            if row_delta == 1 and column_delta == 0:
                row_delta, column_delta = 0, -1
            elif row_delta == -1 and column_delta == 0:
                row_delta, column_delta = 0, 1
            elif row_delta == 0 and column_delta == 1:
                row_delta, column_delta = -1, 0
            elif row_delta == 0 and column_delta == -1:
                row_delta, column_delta = 1, 0

        elif element_on_coordinates == '|':
            if column_delta == 1 or column_delta == -1:
                rays.append((row_index - 1, column_index, -1, 0))
                rays.append((row_index + 1, column_index, 1, 0))
                continue

        elif element_on_coordinates == '-':
            if row_delta == 1 or row_delta == -1:
                rays.append((row_index, column_index - 1, 0, -1))
                rays.append((row_index, column_index + 1, 0, 1))
                continue

        rays.append((row_index + row_delta, column_index + column_delta, row_delta, column_delta))

    return len(set((row_index, column_index) for row_index, column_index, _, _ in visited))


example_input = '''.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....'''.splitlines()

assert solution_for_first_part(example_input) == 46

# The input is taken from: https://adventofcode.com/2023/day/16/input
task_input = list(load_input_file('input.16.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
