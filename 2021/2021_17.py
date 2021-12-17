import re
from typing import Union


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def parse(task_input: str) -> tuple[int, int, int, int]:
    pattern = re.compile(r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)')
    group = pattern.match(task_input)

    return int(group[1]), int(group[2]), int(group[3]), int(group[4])


def run_simulation(xs: int, xe: int, ys: int, ye: int) -> int:

    def is_hit_area(x_velocity: int, y_velocity: int) -> Union[int, None]:
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

            if (xs <= position[0] <= xe) and (ys <= position[1] <= ye):
                return hight

            if position[1] < ys:
                return None


    for x_velocity in range(1, 600):
        for y_velocity in range(-300, 300):
            result = is_hit_area(x_velocity, y_velocity)
            if result != None:
                yield result


def solution_for_first_part(results: list[int]) -> int:
    return max(results)


example_input = 'target area: x=20..30, y=-10..-5'
example_results = list(run_simulation(*parse(example_input)))

assert solution_for_first_part(example_results) == 45

# The input is taken from: https://adventofcode.com/2021/day/17/input
input = load_input_file('input.17.txt')
input_results = list(run_simulation(*parse(input)))

print("Solution for the first part:", solution_for_first_part(input_results))


def solution_for_second_part(result: list[int]) -> int:
    return len(list(result))


assert solution_for_second_part(example_results) == 112
print("Solution for the second part:", solution_for_second_part(input_results))
