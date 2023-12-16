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


def count_energized_titles(mirrors_map: Dict[Tuple[int, int], str], starting_point: Tuple[int, int, int, int]) -> int:
    visited = set()
    rays = [starting_point]

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


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return count_energized_titles(parse(task_input), (0, 0, 0, 1))


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


def solution_for_second_part(task_input: Iterable[str]) -> int:
    mirrors_map = parse(task_input)
    simple = next(iter(mirrors_map))
    row_minium = simple[0]
    row_maxim = simple[0]
    column_minium = simple[1]
    column_maxim = simple[1]

    for row_index, column_index in mirrors_map.keys():
        row_minium = min(row_minium, row_index)
        row_maxim = max(row_maxim, row_index)
        column_minium = min(column_minium, column_index)
        column_maxim = max(column_maxim, column_index)

    result = 0
    for row_index in range(row_minium, row_maxim):
        result = max(count_energized_titles(mirrors_map, (row_index, column_minium, 0, 1)), count_energized_titles(mirrors_map, (row_index, column_maxim, 0, -1)), result)

    for column_index in range(column_minium, column_maxim):
        result = max(count_energized_titles(mirrors_map, (row_minium, column_index, 1, 0)), count_energized_titles(mirrors_map, (row_minium, column_maxim, -1, 0)), result)

    return result


assert solution_for_second_part(example_input) == 51
print("Solution for the second part:", solution_for_second_part(task_input))
