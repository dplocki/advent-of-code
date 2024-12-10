from typing import Dict, Generator, Iterable, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[int, int, int], None, None]:
    for row, line in enumerate(task_input):
        for column, character in enumerate(line):
            yield row, column, int(character)


def find_zero_positions(hiking_map: Dict[Tuple[int, int], int]) -> Generator[Tuple[int, int], None, None]:
    for (row, column), value in hiking_map.items():
        if value == 0:
            yield row, column


def get_path_score(hiking_map: Dict[Tuple[int, int], int], start_zero: Tuple[int, int]) -> int:
    to_check = [ start_zero ]
    result = set()

    while to_check:
        current_position = to_check.pop()
        current_value = hiking_map[current_position]

        if current_value == 9:
            result.add(current_position)
            continue

        for neighbor in ((0, -1), (1, 0), (-1, 0), (0, 1)):
            new_position = current_position[0] + neighbor[0], current_position[1] + neighbor[1]
            if hiking_map.get(new_position, None) == (current_value + 1):
                to_check.append(new_position)

    return len(result)


def solution_for_first_part(task_input: Iterable[str]) -> int:
    hiking_map = {(row, column): value for row, column, value in parse(task_input)}

    return sum(
        get_path_score(hiking_map, zero_position)
        for zero_position in find_zero_positions(hiking_map))


example_input = '''89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732'''.splitlines()

assert solution_for_first_part(example_input) == 36

# The input is taken from: https://adventofcode.com/2024/day/10/input
task_input = list(load_input_file('input.10.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
