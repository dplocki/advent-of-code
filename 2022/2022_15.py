from typing import Generator, Iterable, Tuple
import re


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[int, ...], None, None]:
    for line in task_input:
        yield tuple(map(lambda a: int(a.group()), re.finditer(r'-?\d+', line)))


def manhattan_distance(p1x, p1y, p2x, p2y) -> int:
    return abs(p1x - p2x) + abs(p1y - p2y)


def sign(number: int) -> int:
    return (number > 0) - (number < 0)


def solution_for_first_part(task_input: Iterable[str], y_line: int) -> int:
    lines = list(parse(task_input))

    beacons_x_coordinates_y_line = set()
    visible_fields = set()
    for sensor_x, sensor_y, beacon_x, beacon_y in lines:
        if beacon_y == y_line:
            beacons_x_coordinates_y_line.add(beacon_x)
 
        distance = manhattan_distance(sensor_x, sensor_y, beacon_x, beacon_y) - abs(sensor_y - y_line)
        if distance <= 0:
            continue

        x1 = sensor_x - distance
        x2 = sensor_x + distance

        visible_fields.update(range(x1, x2 + 1, 1))

    return len(visible_fields - beacons_x_coordinates_y_line)


example_input = '''Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3'''.splitlines()

assert solution_for_first_part(example_input, 10) == 26

# The input is taken from: https://adventofcode.com/2022/day/15/input
task_input = list(load_input_file('input.15.txt'))
print("Solution for the first part:", solution_for_first_part(task_input, 2_000_000))
