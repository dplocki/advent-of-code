from typing import Dict, Generator, Iterable, Set, Tuple


DIRECTIONS =  ((0, -1), (1, 0), (-1, 0), (0, 1))


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


def reached_counter_after_one_step(garden_map: Dict[Tuple[int, int], str], points: Iterable[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    result = set()

    for point in points:
        for direction in DIRECTIONS:
            neighbor = point[0] + direction[0], point[1] + direction[1]
            if neighbor in garden_map and garden_map[neighbor] != '#':
                result.add(neighbor)

    return result


def steps_counter(garden_map: Dict[Tuple[int, int], str], start_point: Tuple[int, int], steps: int) -> int:
    points = [start_point]
    for _ in range(steps):
        points = reached_counter_after_one_step(garden_map, points)

    return len(points)


def find_starting_point(garden_map: Dict[Tuple[int, int], str]) -> Tuple[int, int]:
    return next(coordinates for coordinates, tile in garden_map.items() if tile == 'S')


def count_plots_reach_for_steps(task_input: Iterable[str], steps: int) -> int:
    garden_map = parse(task_input)
    return steps_counter(garden_map, find_starting_point(garden_map), steps)


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


def memories_steps_counter(garden_map: Dict[Tuple[int, int], str]):

    memory = {}

    def create_set(start, how_many_steps):
        if (start, how_many_steps) in memory:
            return memory[start, how_many_steps]

        if how_many_steps == 0:
            memory[start, 0] = [start]
            return memory[start, 0]

        result = reached_counter_after_one_step(garden_map, create_set(start, how_many_steps - 1))
        memory[start, how_many_steps] = result

        return result


    def internal(start, how_many_steps):
        if (start, how_many_steps) in memory:
            return len(memory[start, how_many_steps])

        if how_many_steps == 0:
            return 0

        result = reached_counter_after_one_step(garden_map, create_set(start, how_many_steps - 1))
        memory[start, how_many_steps] = result

        return len(result)

    return internal


def solution_for_second_part(task_input: Iterable[str]) -> int:
    MAX_STEPS = 26501365
    garden_map = parse(task_input)
    internal_steps_counter = memories_steps_counter(garden_map)

    max_row_index, max_column_index = 0, 0
    for row_index, column_index in garden_map.keys():
        max_row_index = max(row_index, max_row_index)
        max_column_index = max(column_index, max_column_index)

    assert max_row_index == max_column_index
    size = max_row_index + 1

    past_whole_grids = MAX_STEPS // size - 1

    start = find_starting_point(garden_map)

    odd_grids = (past_whole_grids // 2 * 2 + 1) ** 2
    even_grids = ((past_whole_grids + 1) // 2 * 2) ** 2

    left_steps = size // 2 - 1

    ne_smaller = internal_steps_counter((size - 1, 0), left_steps)
    se_smaller = internal_steps_counter((0, 0), left_steps)
    sw_smaller = internal_steps_counter((0, size - 1), left_steps)
    nw_smaller = internal_steps_counter((size - 1, size - 1), left_steps)

    left_steps = size * 3 // 2 - 1

    ne_larger = internal_steps_counter((size - 1, 0), left_steps)
    se_larger = internal_steps_counter((0, 0), left_steps)
    sw_larger = internal_steps_counter((0, size - 1), left_steps)
    nw_larger = internal_steps_counter((size - 1, size - 1), left_steps)

    return (
            odd_grids * internal_steps_counter(start, 2 * size - 1)
            + even_grids * internal_steps_counter(start, 2 * size)

            + internal_steps_counter((size - 1, size // 2), size - 1)
            + internal_steps_counter((size // 2, 0), size - 1)
            + internal_steps_counter((0, size // 2), size - 1)
            + internal_steps_counter((size // 2, size - 1), size - 1)

            + (past_whole_grids + 1) * (ne_smaller + se_smaller + sw_smaller + nw_smaller)
            + past_whole_grids * (ne_larger + se_larger + sw_larger + nw_larger)
       )

print("Solution for the second part:", solution_for_second_part(task_input))
