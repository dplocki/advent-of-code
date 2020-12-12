DIRECTION_ROTATE_RIGHT = 'ESWN'
DIRECTION_NUMBER = len(DIRECTION_ROTATE_RIGHT)
DIRECTION_VECTOR = {
    'E': (1, 0),
    'S': (0, -1),
    'W': (-1, 0),
    'N': (0, 1)
}


def load_input_file(file_name: str) -> [str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: [str]) -> [tuple]:
    for line in task_input:
        yield line[0], int(line[1:])


def move(direction: int, value: int, coordinates: tuple) -> tuple:
    d = DIRECTION_VECTOR[direction]
    return coordinates[0] + d[0] * value, coordinates[1] + d[1] * value


def solution_for_first_part(task_input: [tuple]) -> int:

    def turn_right(facing: str, value: int) -> str:
        return DIRECTION_ROTATE_RIGHT[(DIRECTION_ROTATE_RIGHT.index(facing) + (value // 90)) % DIRECTION_NUMBER]


    ship = 0, 0
    facing = 'E'

    for instruction, value in parse(task_input):
        if instruction in DIRECTION_VECTOR:
            ship = move(instruction, value, ship)
        elif instruction == 'R':
            facing = turn_right(facing, value)
        elif instruction == 'L':
            facing = turn_right(facing, -value)
        elif instruction == 'F':
            ship = move(facing, value, ship)

    return sum(map(abs, ship))


example_input = '''F10
N3
F7
R90
F11'''.splitlines()

assert solution_for_first_part(example_input) == 25

# The input is taken from: https://adventofcode.com/2020/day/12/input
task_input = list(load_input_file('input.12.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input):

    def turn_right(value, waypoint):
        x, y = waypoint
        if value % 360 == 0:
            return x, y
        elif value % 360 == 90:
            return y, -x
        elif value % 360 == 180:
            return -x, -y
        elif value % 360 == 270:
            return -y, x


    ship = 0, 0
    waypoint = 10, 1

    for instruction, value in parse(task_input):
        if instruction in DIRECTION_VECTOR:
            waypoint = move(instruction, value, waypoint)
        elif instruction == 'R':
            waypoint = turn_right(value, waypoint)
        elif instruction == 'L':
            waypoint = turn_right(abs(360 - value), waypoint)
        elif instruction == 'F':
            ship = ship[0] + waypoint[0] * value, ship[1] + waypoint[1] * value

    return sum(map(abs, ship))



assert solution_for_second_part(example_input) == 286
print("Solution for the first part:", solution_for_second_part(task_input))
