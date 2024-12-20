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


def get_all_available_shortcuts(task_input: Iterable[str]) -> Dict[int, int]:
    maze, begin, end = parse(task_input)
    visited = build_path_dictionary(maze, begin, end)
    result = {}

    for point, type_of_tile in maze.items():
        if type_of_tile != '#':
            continue

        neighborA = point[0] - 1, point[1]
        neighborB = point[0] + 1, point[1]

        if neighborA in visited and neighborB in visited:
            save = abs(visited[neighborA] - visited[neighborB]) - 2
            result[save] = result.get(save, 0) + 1

        neighborA = point[0], point[1] - 1
        neighborB = point[0], point[1] + 1

        if neighborA in visited and neighborB in visited:
            save = abs(visited[neighborA] - visited[neighborB]) -2
            result[save] = result.get(save, 0) + 1

    return result


def solution_for_first_part(task_input: Iterable[str]) -> int:
    results = get_all_available_shortcuts(task_input)

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

example_result = get_all_available_shortcuts(example_input)

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
