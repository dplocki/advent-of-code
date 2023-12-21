from typing import Dict, Generator, Iterable, Set, Tuple


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Dict[Tuple[int, int], str]:
    return {
            (row_index, column_index): character
            for row_index, line in enumerate(task_input)
            for column_index, character in enumerate(line)
        }


def steps_counter(garden_map: Dict[Tuple[int, int], str], points: Iterable[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    result = set()

    for point in points:
        for direction in ((0, -1), (1, 0), (-1, 0), (0, 1)):
            neighbor = point[0] + direction[0], point[1] + direction[1]
            if neighbor in garden_map and garden_map[neighbor] != '#':
                result.add(neighbor)

    return result


def count_plots_reach_for_steps(task_input: Iterable[str], steps: int) -> int:
    garden_map = parse(task_input)

    start = next(coordinates for coordinates, tile in garden_map.items() if tile == 'S')
    garden_map[start] = '.'

    points = [start]
    for _ in range(steps):
        points = steps_counter(garden_map, points)

    return len(points)


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return count_plots_reach_for_steps(task_input, 64)


example_input = '''...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........'''.splitlines()

assert count_plots_reach_for_steps(example_input, 6) == 16

# The input is taken from: https://adventofcode.com/2023/day/21/input
task_input = list(load_input_file('input.21.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
