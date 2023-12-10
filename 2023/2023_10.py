from typing import Dict, Generator, Iterable, Set, Tuple


EMPTY_FIELD = (False, False, False, False)


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]):
    result = {}

    for row_index,  line in enumerate(task_input):
        for column_index, character in enumerate(line):
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
        elif value == '.':
            result[point] = EMPTY_FIELD

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

    return cost_so_far


def solution_for_first_part(task_input: Iterable[str]) -> int:
    raw_map = parse(task_input)
    pipe_schematic = transform_map_to_pipe_schematic(raw_map)

    starting_position = next(c for c, v in raw_map.items() if v == 'S')
    pipe_schematic[starting_position] = deduct_starting_point(starting_position, pipe_schematic)

    pipe_distance_from_start = bfs(pipe_schematic, starting_position)

    return max(pipe_distance_from_start.values())


example_input = '''..F7.
.FJ|.
SJ.L7
|F--J
LJ...'''.splitlines()

assert solution_for_first_part(example_input) == 8

# The input is taken from: https://adventofcode.com/2023/day/10/input
task_input = list(load_input_file('input.10.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def get_neighbors_from_pipe_schematic(pipe_schematic: Dict[Tuple[int, int], Tuple[bool, bool, bool, bool]], point: Tuple[int, int]) -> Generator[Tuple[int, int], None, None]:
    row, column = point
    if (row // 2, column // 2) not in pipe_schematic:
        return

    schema = pipe_schematic[row // 2, column // 2]

    if row % 2 == 0:
        yield row - 1, column

        if (column % 2 == 0 and not schema[3]) or (column % 2 == 1 and not schema[1]):
            yield row + 1, column
    else:
        if (column % 2 == 0 and not schema[3]) or (column % 2 == 1 and not schema[1]):
            yield row - 1, column

        yield row + 1, column

    if column % 2 == 0:
        yield row, column - 1

        if (row % 2 == 0 and not schema[0]) or (row % 2 == 1 and not schema[2]):
            yield row, column + 1
    else:
        if (row % 2 == 0 and not schema[0]) or (row % 2 == 1 and not schema[2]):
            yield row, column - 1

        yield row, column + 1


def find_outsiders_elements(pipe_schematic: Dict[Tuple[int, int], Tuple[bool, bool, bool, bool]]) -> Set[Tuple[int, int]]:
    to_check = [(0, 0)]
    rescaled_outside = set()

    while to_check:
        point = to_check.pop()
        if point in rescaled_outside:
            continue

        rescaled_outside.add(point)

        for p in get_neighbors_from_pipe_schematic(pipe_schematic, point):
            to_check.append(p)

    result = set()
    for point in rescaled_outside:
        if point[0] % 2 != 0 or point[1] % 2 != 0:
            continue

        row = (point[0] // 2) * 2
        column = (point[1] // 2) * 2

        if  (row,     column    ) in rescaled_outside and \
            (row + 1, column    ) in rescaled_outside and \
            (row + 1, column + 1) in rescaled_outside and \
            (row,     column + 1) in rescaled_outside:
            result.add((row, column))

    return result


def solution_for_second_part(task_input: Iterable[str]) -> int:
    raw_map = parse(task_input)
    pipe_schematic = transform_map_to_pipe_schematic(raw_map)
    starting_position = next(c for c, v in raw_map.items() if v == 'S')
    pipe_schematic[starting_position] = deduct_starting_point(starting_position, pipe_schematic)
    main_loop_pipes_positions = bfs(pipe_schematic, starting_position).keys()
    clean_schematic_map = {
        key:(value if key in main_loop_pipes_positions else EMPTY_FIELD)
        for key, value in pipe_schematic.items()
    }

    outsiders_elements = find_outsiders_elements(clean_schematic_map)

    return len(pipe_schematic) - len(main_loop_pipes_positions) - len(outsiders_elements)


example_input_1 = '''.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...'''.splitlines()

assert solution_for_second_part(example_input_1) == 8

example_input_2 = '''FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L'''.splitlines()

assert solution_for_second_part(example_input_2) == 10

print("Solution for the second part:", solution_for_second_part(task_input))
