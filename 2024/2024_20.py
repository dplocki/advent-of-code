from itertools import permutations
from typing import Dict, Generator, Iterable, Tuple


NEIGHBORS = (0, -1), (1, 0), (-1, 0), (0, 1)


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Tuple[Dict[Tuple[int, int], str], int, int]:
    maze = {(row, column): character
        for row, line in enumerate(task_input)
        for column, character in enumerate(line)}

    begin = None
    end = None
    for (position, letter) in maze.items():
        if letter == 'S':
            begin = position
        elif letter == 'E':
            end = position

    maze[begin] = '.'
    maze[end] = '.'

    return maze, begin, end


def build_path_dictionary(maze: Dict[Tuple[int, int], str], start: Tuple[int, int], end: Tuple[int, int]) -> Dict[Tuple[int, int], int]:
    step_counter = 0
    visited = { }
    current_point = start

    while current_point:
        visited[current_point] = step_counter

        if current_point == end:
            return visited

        step_counter += 1

        for neighbor in NEIGHBORS:
            new_position = current_point[0] + neighbor[0], current_point[1] + neighbor[1]
            if new_position in maze and maze[new_position] != '#' and new_position not in visited:
                current_point = new_position
                break


def manhattan_distance(point_from: Tuple[int, int], point_to: Tuple[int, int]) -> int:
    return abs(point_from[0] - point_to[0]) + abs(point_from[1] - point_to[1])


def get_all_available_shortcuts(task_input: Iterable[str], maximum_distance: int) -> int:
    maze, begin, end = parse(task_input)
    visited = build_path_dictionary(maze, begin, end)
    result = {}

    for from_point, to_point in permutations(visited.keys(), 2):
        distance = manhattan_distance(from_point, to_point)
        if distance > maximum_distance:
            continue

        save = visited[from_point] - visited[to_point] - distance
        result[save] = result.get(save, 0) + 1

    return result


def solution_for_first_part(task_input: Iterable[str]) -> int:
    results = get_all_available_shortcuts(task_input, 2)

    return sum(how_many for save, how_many in results.items() if save >= 100)


example_input = '''###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############'''.splitlines()

example_result = get_all_available_shortcuts(example_input, 2)

assert example_result[2] == 14
assert example_result[4] == 14
assert example_result[6] == 2
assert example_result[8] == 4
assert example_result[10] == 2
assert example_result[12] == 3
assert example_result[20] == 1
assert example_result[36] == 1
assert example_result[38] == 1
assert example_result[40] == 1
assert example_result[64] == 1

# The input is taken from: https://adventofcode.com/2024/day/20/input
task_input = list(load_input_file('input.20.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> int:
    results = get_all_available_shortcuts(task_input, 20)

    return sum(how_many for save, how_many in results.items() if save >= 100)


example_result = get_all_available_shortcuts(example_input, 20)

assert example_result[50] == 32
assert example_result[52] == 31
assert example_result[54] == 29
assert example_result[56] == 39
assert example_result[58] == 25
assert example_result[60] == 23
assert example_result[62] == 20
assert example_result[64] == 19
assert example_result[66] == 12
assert example_result[68] == 14
assert example_result[70] == 12
assert example_result[72] == 22
assert example_result[74] == 4
assert example_result[76] == 3

print("Solution for the second part:", solution_for_second_part(task_input))
