from typing import Dict, Generator, Iterable, Tuple


EMPTY_FIELD = (False, False, False, False)


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]):
    result = {}

    for row_index,  line in enumerate(task_input):
        for column_index, character in enumerate(line):
            if character != '.':
                result[row_index, column_index] = character

    return result


def transform_map_to_pipe_schematic(raw_map: Dict[Tuple[int, int], str]) -> Dict[Tuple[int, int], Tuple[bool, bool, bool, bool]]:
    result = {}

    for point, value in raw_map.items():
        if value == '|':
            result[point] = (True, False, True, False)
        elif value == '-':
            result[point] = (False, True, False, True)
        elif value == 'L':
            result[point] = (True, True, False, False)
        elif value == 'J':
            result[point] = (True, False, False, True)
        elif value == '7':
            result[point] = (False, False, True, True)
        elif value == 'F':
            result[point] = (False, True, True, False)

    return result


def deduct_starting_point(start_point: Tuple[int, int], pipe_schematic: Dict[Tuple[int, int], Tuple[bool, bool, bool, bool]]):
    return (
        pipe_schematic.get((start_point[0] - 1, start_point[1]), EMPTY_FIELD)[2],
        pipe_schematic.get((start_point[0], start_point[1] + 1), EMPTY_FIELD)[3],
        pipe_schematic.get((start_point[0] + 1, start_point[1]), EMPTY_FIELD)[0],
        pipe_schematic.get((start_point[0], start_point[1] - 1), EMPTY_FIELD)[1]
    )


def get_neighbors(pipe_schematic: Dict[Tuple[int, int], Tuple[bool, bool, bool, bool]], row_index: int, column_index: int) -> Generator[Tuple[int, int], None, None]:
    schema = pipe_schematic[row_index, column_index]

    if schema[0]:
        yield row_index - 1, column_index

    if schema[1]:
        yield row_index, column_index + 1

    if schema[2]:
        yield row_index + 1, column_index

    if schema[3]:
        yield row_index, column_index - 1


def bfs(pipe_schematic: Dict[Tuple[int, int], Tuple[bool, bool, bool, bool]], start: Tuple[int, int]) -> int:
    to_check = [start]
    cost_so_far = dict()
    cost_so_far[start] = 0

    while to_check:
        row_index, column_index = to_check.pop()

        for new_point in get_neighbors(pipe_schematic, row_index, column_index):
            new_cost = cost_so_far[row_index, column_index] + 1

            if new_point not in cost_so_far or new_cost < cost_so_far[new_point]:
                cost_so_far[new_point] = new_cost
                to_check.append(new_point)

    return max(cost_so_far.values())


def solution_for_first_part(task_input: Iterable[str]) -> int:
    raw_map = parse(task_input)
    pipe_schematic = transform_map_to_pipe_schematic(raw_map)

    starting_position = next(c for c, v in raw_map.items() if v == 'S')
    pipe_schematic[starting_position] = deduct_starting_point(starting_position, pipe_schematic)

    return bfs(pipe_schematic, starting_position)


example_input = '''..F7.
.FJ|.
SJ.L7
|F--J
LJ...'''.splitlines()

assert solution_for_first_part(example_input) == 8

# The input is taken from: https://adventofcode.com/2023/day/10/input
task_input = list(load_input_file('input.10.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
