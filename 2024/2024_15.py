from functools import cache
from typing import Dict, Generator, Iterable, Tuple


ROW = 0
COLUMN = 1

FLOOR = '.'
BOX = 'O'
WALL = '#'

LEFT_BOX_PART = '['
RIGHT_BOX_PART = ']'


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def parse_move_list(task_input: str) -> Generator[str, None, None]:
    yield from(
        character
        for line in task_input
        for character in line
        if character in '<^>v'
    )


def parse(task_input: str) -> Tuple[Dict[Tuple[int, int], str], Tuple[int, int], Generator[str, None, None]]:
    raw_warehouse_map, raw_robot_movements = task_input.split('\n\n')
    start = None

    warehouse_map = {}
    for row, line in enumerate(raw_warehouse_map.splitlines()):
        for column, character in enumerate(line):
            if character == WALL or character == FLOOR or character == BOX:
                warehouse_map[row, column] = character
            elif character == '@':
                warehouse_map[row, column] = FLOOR
                start = (row, column)

    return warehouse_map, start, parse_move_list(raw_robot_movements)


def move_boxes(warehouse_map: Dict[Tuple[int, int], str], start: Tuple[int, int], vector: Tuple[int, int], what: str) -> None:
    current = warehouse_map[start]
    if current != FLOOR:
        move_boxes(warehouse_map, (start[ROW] + vector[ROW], start[COLUMN] + vector[COLUMN]), vector, current)

    warehouse_map[start] = what


def can_be_moved(warehouse_map: Dict[Tuple[int, int], str], location: Tuple[int, int], where: Tuple[int, int]) -> bool:
    if warehouse_map[where] == FLOOR:
        return True

    if warehouse_map[where] == BOX:
        return can_be_moved(warehouse_map, where, (where[ROW] + (where[ROW] - location[ROW]), where[COLUMN] + (where[COLUMN] - location[COLUMN])))

    return False


def solution_for_first_part(task_input: Iterable[str]) -> int:
    warehouse_map, robot_position, movements = parse(task_input)

    for move in movements:
        if move == '<':
            vector = 0, -1
        elif move == '>':
            vector = 0, 1
        elif move == '^':
            vector = -1, 0
        elif move == 'v':
            vector = 1, 0

        new_robot_position = robot_position[ROW] + vector[ROW], robot_position[COLUMN] + vector[COLUMN]
        if can_be_moved(warehouse_map, robot_position, new_robot_position):
            robot_position = new_robot_position
            move_boxes(warehouse_map, new_robot_position, vector, FLOOR)

    return sum(
        location[ROW] * 100 + location[COLUMN]
        for location, what in warehouse_map.items()
        if what == BOX
    )


smaller_example_input = '''########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<'''

larger_example_input = '''##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^'''

assert solution_for_first_part(smaller_example_input) == 2028
assert solution_for_first_part(larger_example_input) == 10092

# The input is taken from: https://adventofcode.com/2024/day/15/input
task_input = load_input_file('input.15.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


def parse_wider_box(task_input: str) -> Tuple[Dict[Tuple[int, int], str], Tuple[int, int], Iterable[str]]:
    raw_warehouse_map, raw_robot_movements = task_input.split('\n\n')
    start = None

    warehouse_map = {}
    for row, line in enumerate(raw_warehouse_map.splitlines()):
        for column, character in enumerate(line):
            if character == WALL or character == FLOOR:
                warehouse_map[row, column * 2] = character
                warehouse_map[row, column * 2 + 1] = character
            elif character == BOX:
                warehouse_map[row, column * 2] = LEFT_BOX_PART
                warehouse_map[row, column * 2 + 1] = RIGHT_BOX_PART
            elif character == '@':
                warehouse_map[row, column * 2] = FLOOR
                warehouse_map[row, column * 2 + 1] = FLOOR
                start = (row, column * 2)

    return warehouse_map, start, parse_move_list(raw_robot_movements)


def move_wider_boxes(warehouse_map: Dict[Tuple[int, int], str], where: Tuple[int, int], vector: Tuple[int, int], what: str) -> None:
    current = warehouse_map[where]

    if vector[COLUMN] == -1:
        if current == RIGHT_BOX_PART:
            move_wider_boxes(warehouse_map, (where[ROW], where[COLUMN] - 1), vector, current)
            move_wider_boxes(warehouse_map, (where[ROW], where[COLUMN] - 2), vector, LEFT_BOX_PART)

    elif vector[COLUMN] == 1:
        if current == LEFT_BOX_PART:
            move_wider_boxes(warehouse_map, (where[ROW], where[COLUMN] + 1), vector, current)
            move_wider_boxes(warehouse_map, (where[ROW], where[COLUMN] + 2), vector, RIGHT_BOX_PART)

    if current == FLOOR or vector[ROW] == 0:
        warehouse_map[where] = what
        return

    boxes_to_moves = {}
    to_check = [where]
    while to_check:
        current = to_check.pop()
        if current in boxes_to_moves:
            continue

        what = warehouse_map[current]
        if what == FLOOR:
            continue

        boxes_to_moves[current] = what
        if what == LEFT_BOX_PART:
            to_check.append((current[ROW], current[COLUMN] + 1))

            to_check.append((current[ROW] + vector[ROW], current[COLUMN] + vector[COLUMN]))
            to_check.append((current[ROW] + vector[ROW], current[COLUMN] + 1 + vector[COLUMN]))
        elif what == RIGHT_BOX_PART:
            to_check.append((current[ROW], current[COLUMN] - 1))

            to_check.append((current[ROW] + vector[ROW], current[COLUMN] + vector[COLUMN]))
            to_check.append((current[ROW] + vector[ROW], current[COLUMN] - 1 + vector[COLUMN]))

    for key in boxes_to_moves.keys():
        warehouse_map[key] = FLOOR

    for key, value in boxes_to_moves.items():
        warehouse_map[key[ROW] + vector[ROW], key[COLUMN] + vector[COLUMN]] = value


def can_be_moved_wider_box(warehouse_map: Dict[Tuple[int, int], str], where, vector):
    if warehouse_map[where] == FLOOR:
        return True

    if warehouse_map[where] == WALL:
        return False

    if vector[COLUMN] != 0:
        return can_be_moved_wider_box(warehouse_map, (where[ROW], where[COLUMN] + vector[COLUMN]), vector)

    if vector[ROW] != 0:
        part_in_line = can_be_moved_wider_box(warehouse_map, (where[ROW] + vector[ROW], where[COLUMN]), vector)
        if warehouse_map[where] == RIGHT_BOX_PART:
            return part_in_line and can_be_moved_wider_box(warehouse_map, (where[ROW] + vector[ROW], where[COLUMN] - 1), vector)

    return part_in_line and can_be_moved_wider_box(warehouse_map, (where[ROW] + vector[ROW], where[COLUMN] + 1), vector)


def solution_for_second_part(task_input: Iterable[str]) -> int:
    warehouse_map, robot_position, movements = parse_wider_box(task_input)

    for move in movements:
        if move == '<':
            vector = 0, -1
        elif move == '>':
            vector = 0, 1
        elif move == '^':
            vector = -1, 0
        elif move == 'v':
            vector = 1, 0

        new_robot_position = robot_position[ROW] + vector[ROW], robot_position[COLUMN] + vector[COLUMN]
        if can_be_moved_wider_box(warehouse_map, new_robot_position, vector):
            robot_position = new_robot_position
            move_wider_boxes(warehouse_map, new_robot_position, vector, FLOOR)

    return sum(
        location[ROW] * 100 + location[COLUMN]
        for location, what in warehouse_map.items()
        if what == LEFT_BOX_PART
    )


assert solution_for_second_part(larger_example_input) == 9021
print("Solution for the second part:", solution_for_second_part(task_input))
