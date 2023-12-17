from typing import Dict, Generator, Iterable, List, Tuple
from heapq import heappop, heappush


DIRECTIONS = ((0, -1), (1, 0), (-1, 0), (0, 1))


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Dict[Tuple[int, int], int]:
    return {(row_index, column_index): int(character)
            for row_index, line in enumerate(task_input)
            for column_index, character in enumerate(line)}


def heuristic(current_point: tuple[int, int], target: tuple[int, int]) -> int:
    return abs(current_point[0] - target[0]) + abs(current_point[1] - target[1])


def find_crucible_path_cost(heat_loss_map: Dict[Tuple[int, int], int], start: Tuple[int, int], end: Tuple[int, int]) -> int:
    visited = set()
    possibilities = []
    for direction in DIRECTIONS:
        new_point = start[0] + direction[0], start[1] + direction[1]
        if new_point in heat_loss_map:
            heappush(possibilities, (heat_loss_map[new_point], new_point, direction, 1))

    while possibilities:
        cost, current_point, last_direction, direction_counter = heappop(possibilities)

        if (current_point, last_direction, direction_counter) in visited:
            continue
        else:
            visited.add((current_point, last_direction, direction_counter))

        if current_point == end:
            return cost

        for direction in DIRECTIONS:
            next_point = current_point[0] + direction[0], current_point[1] + direction[1]
            if next_point not in heat_loss_map:
                continue

            if (direction[0] + last_direction[0], direction[1] + last_direction[1]) == (0, 0):
                continue

            new_direction_counter = (direction_counter + 1) if last_direction == direction else 1
            if new_direction_counter > 3:
                continue

            new_cost = heat_loss_map[next_point] + cost
            heappush(possibilities, (new_cost, next_point, direction, new_direction_counter))


def solution_for_first_part(task_input: Iterable[str]) -> int:
    heat_loss_map = parse(task_input)

    simple = next(iter(heat_loss_map))
    row_maxim = simple[0]
    column_maxim = simple[1]

    for row_index, column_index in heat_loss_map.keys():
        row_maxim = max(row_maxim, row_index)
        column_maxim = max(column_maxim, column_index)

    return find_crucible_path_cost(heat_loss_map, (0, 0), (row_maxim, column_maxim))


example_input = '''2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533'''.splitlines()

assert solution_for_first_part(example_input) == 102

# The input is taken from: https://adventofcode.com/2023/day/17/input
task_input = list(load_input_file('input.17.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
