from typing import Dict, Generator, Iterable, List, Tuple


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[List[Tuple[int, int]], None, None]:
    for line in task_input:
        tokens = line.split(' -> ')
        yield list(tuple(map(int, t.split(','))) for t in tokens)

    return


def sign(number: int) -> int:
    return (number > 0) - (number < 0)


def build_map(lines: Generator[List[Tuple[int, int]], None, None]) -> Dict[Tuple[int, int], str]:
    result = {}

    for line in lines:
        for start_point, end_point in zip(line, line[1:]):
            dx = end_point[0] - start_point[0]
            dy = end_point[1] - start_point[1]

            if dx != 0:
                delta_sign = sign(dx)
                for new_x in range(start_point[0], end_point[0] + delta_sign, delta_sign):
                    result[new_x, end_point[1]] = '#'
            elif dy != 0:
                delta_sign = sign(dy)
                for new_y in range(start_point[1], end_point[1] + delta_sign, delta_sign):
                    result[end_point[0], new_y] = '#'

    return result


def sand_sim(cave_map: Dict[Tuple[int, int], str], bottom: int) -> Tuple[int, int]:
    x, y = 500, 0

    while True:
        if y < bottom:
            if cave_map.get((x, y + 1), '.') == '.':
                y += 1
                continue
        
            if cave_map.get((x - 1, y + 1), '.') == '.':
                y += 1
                x -= 1
                continue

            if cave_map.get((x + 1, y + 1), '.') == '.':
                y += 1
                x += 1
                continue

        return x, y


def solution_for_first_part(task_input: Iterable[str]) -> int:
    cave_map = build_map(parse(task_input))
    bottom = max(y for _, y in cave_map.keys()) + 1

    sand = 0
    while True:
        x, y = sand_sim(cave_map, bottom)
        cave_map[x, y] = 's'
        if y >= bottom:
            return sand
        else:
            sand += 1


example_input = '''498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9'''.splitlines()

assert solution_for_first_part(example_input) == 24

# The input is taken from: https://adventofcode.com/2022/day/14/input
task_input = list(load_input_file('input.14.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> int:
    cave_map = build_map(parse(task_input))
    bottom = max(y for _, y in cave_map.keys()) + 1

    sand = 1
    while True:
        x, y = sand_sim(cave_map, bottom)
        if (x, y) == (500, 0):
            return sand
        else:
            cave_map[x, y] = 's'
            sand += 1


assert solution_for_second_part(example_input) == 93
print("Solution for the second part:", solution_for_second_part(task_input))
