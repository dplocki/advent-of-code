import re


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def parse(task_input: str) -> tuple[int, int, int, int]:
    pattern = re.compile(r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)')
    group = pattern.match(task_input)

    return int(group[1]), int(group[2]), int(group[3]), int(group[4])


def is_hit_area(x_velocity, y_velocity, xs, xe, ys, ye):
    hight = 0
    velocity = (x_velocity, y_velocity)
    position = (0, 0)

    while True:
        position = (position[0] + velocity[0], position[1] + velocity[1])
        hight = max(hight, position[1])

        if velocity[0] > 0:
            velocity = (velocity[0] - 1, velocity[1] - 1)
        elif velocity[0] < 0:
            velocity = (velocity[0] + 1, velocity[1] - 1)
        else:
            velocity = (velocity[0], velocity[1] - 1)
            if not (xs < position[0] < xe):
                return None

        if (xs <= position[0] <= xe) and (ye <= position[1] <= ys):
            return hight

        if position[1] < ys:
            return None


def solution_for_first_part(task_input):
    xs, xe, ye, ys = list(parse(task_input))
    maxium_hight = 0

    for x_velocity in range(1, 300):
        for y_velocity in range(0, 300):
            result = is_hit_area(x_velocity, y_velocity, xs, xe, ys, ye)
            if result != None:
                maxium_hight = max(maxium_hight, result)

    return maxium_hight


example_input = 'target area: x=20..30, y=-10..-5'

assert solution_for_first_part(example_input) == 45

# The input is taken from: https://adventofcode.com/2021/day/17/input
result = solution_for_first_part(load_input_file('input.17.txt'))
print("Solution for the first part:", result)
