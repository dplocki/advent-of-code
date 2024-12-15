from typing import Dict, Iterable, Tuple


FLOOR = '.'
BOX = 'O'
WALL = '#'


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def parse(task_input: str) -> Tuple[Dict[Tuple[int, int], str], Tuple[int, int], Iterable[str]]:
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

    movements = [
        character
        for line in raw_robot_movements
        for character in line
        if character in '<^>v'
    ]

    return warehouse_map, start, movements


def move_boxes(warehouse_map: Dict[Tuple[int, int], str], start: Tuple[int, int], vector: Tuple[int, int], what: str) -> None:
    current = warehouse_map[start]
    if current != FLOOR:
        move_boxes(warehouse_map, (start[0] + vector[0], start[1] + vector[1]), vector, current)

    warehouse_map[start] = what


def can_be_moved(warehouse_map: Dict[Tuple[int, int], str], location: Tuple[int, int], where: Tuple[int, int]) -> bool:
    if warehouse_map[where] == FLOOR:
        return True

    if warehouse_map[where] == BOX:
        return can_be_moved(warehouse_map, where, (where[0] + (where[0] - location[0]), where[1] + (where[1] -location[1])))

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

        new_robot_position = robot_position[0] + vector[0], robot_position[1] + vector[1]
        if can_be_moved(warehouse_map, robot_position, new_robot_position):
            robot_position = new_robot_position
            move_boxes(warehouse_map, new_robot_position, vector, FLOOR)

    return sum(
        location[0] * 100 + location[1]
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
