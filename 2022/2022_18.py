import itertools
from typing import Generator, Iterable, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]):
    for line in task_input:
        yield tuple(map(int, line.split(',')))


def manhattan_distance(point1: Tuple[int, int, int], point2: Tuple[int, int, int]) -> int:
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1]) + abs(point1[2] - point2[2])


def count_all_sides_of_cubes(cubes: Iterable[Tuple[int, int, int]]) -> int:
    result = len(cubes) * 6

    for c1, c2 in itertools.combinations(cubes, 2):
        if manhattan_distance(c1, c2) == 1:
            result -= 2

    return result


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return count_all_sides_of_cubes(list(parse(task_input)))


example_input = '''2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5'''.splitlines()

assert solution_for_first_part(example_input) == 64
# The input is taken from: https://adventofcode.com/2022/day/18/input
task_input = list(load_input_file('input.18.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> int:
    cubes = set(parse(task_input))

    xs = [x for x, _, _ in cubes]
    ys = [y for _, y, _ in cubes]
    zs = [z for _, _, z in cubes]
    max_x = max(xs) + 1
    max_y = max(ys) + 1
    max_z = max(zs) + 1
    min_x = min(xs) - 1
    min_y = min(ys) - 1
    min_z = min(zs) - 1
    
    internal_cubes = set()
    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            for z in range(min_z, max_z):
                if (x, y, z) not in cubes:
                    internal_cubes.add((x, y, z))

    todo = [(min_x + 1, min_y + 1, min_y + 1)]
    while todo:
        point = todo.pop()
        if point not in internal_cubes:
            continue

        internal_cubes.remove(point)
        todo.append((point[0] - 1, point[1], point[2]))
        todo.append((point[0] + 1, point[1], point[2]))
        todo.append((point[0], point[1] - 1, point[2]))
        todo.append((point[0], point[1] + 1, point[2]))
        todo.append((point[0], point[1], point[2] - 1))
        todo.append((point[0], point[1], point[2] + 1))

    result = count_all_sides_of_cubes(cubes)
    for c, i in itertools.product(cubes, internal_cubes):
        if manhattan_distance(c, i) == 1:
            result -= 1

    return result


assert solution_for_second_part(example_input) == 58
print("Solution for the second part:", solution_for_second_part(task_input))
