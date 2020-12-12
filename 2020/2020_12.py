from enum import IntEnum, unique


@unique
class Direction(IntEnum):
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3


DIRECTION_ROTATE_RIGHT = 'ESWN'
DIRECTION_NUMBER = len(DIRECTION_ROTATE_RIGHT)
DIRECTION_VECTOR = {
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0),
    Direction.NORTH: (0, -1)
}


def load_input_file(file_name: str) -> [str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: [str]) -> [tuple]:
    for line in task_input:
        yield line[0], int(line[1:])


def solution_for_first_part(task_input: [tuple]) -> int:

    def move(direction: int, x: int, y: int) -> int:
        dx, dy = DIRECTION_VECTOR[direction]
        return x + dx * value, y + dy * value


    def turn_right(facing: Direction, value: int) -> Direction:
        return Direction((facing + (value // 90)) % DIRECTION_NUMBER)


    x, y = 0, 0
    facing = Direction.EAST

    for instruction, value in list(parse(task_input)):
        if instruction in DIRECTION_ROTATE_RIGHT:
            x, y = move(DIRECTION_ROTATE_RIGHT.index(instruction), x, y)
        elif instruction == 'R':
            facing = turn_right(facing, value)
        elif instruction == 'L':
            facing = turn_right(facing, -value)
        elif instruction == 'F':
            x, y = move(facing, x, y)

    return abs(x) + abs(y)


example_input = '''F10
N3
F7
R90
F11'''.splitlines()

assert solution_for_first_part(example_input) == 25

# The input is taken from: https://adventofcode.com/2020/day/12/input
task_input = list(load_input_file('input.12.txt'))
result = solution_for_first_part(task_input)
print("Solution for the first part:", result)
