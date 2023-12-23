from typing import Callable, Dict, Generator, Iterable, Set, Tuple
import collections


DIRECTIONS = ((0, -1), (1, 0), (-1, 0), (0, 1))


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Tuple[int, int]:
    return {
        (row_index, column_index): character
        for row_index, line in enumerate(task_input)
        for column_index, character in enumerate(line)}


def get_all_neighbors(hiking_map: Tuple[int, int], point: Tuple[int, int]) -> Generator[Tuple[int, int], None, None]:
    for direction in DIRECTIONS:
        new_point = point[0] + direction[0], point[1] + direction[1]
        if new_point not in hiking_map or hiking_map[new_point] == '#':
            continue

        yield new_point


def get_neighbors_with_slops(hiking_map: Dict[Tuple[int, int], str], point: Tuple[int, int]) -> Generator[Tuple[int, int], None, None]:
    if hiking_map[point] == 'v':
        yield point[0] + 1, point[1]

    elif hiking_map[point] == '^':
        yield point[0] - 1, point[1]

    elif hiking_map[point] == '>':
        yield point[0], point[1] + 1

    elif hiking_map[point] == 'v':
        yield point[0], point[1] - 1

    else:
        yield from get_all_neighbors(hiking_map, point)


def find_the_longest_path(get_all_neighbors: Callable[[Dict[Tuple[int, int], str]], Iterable[Tuple[int, int]]], hiking_map: Dict[Tuple[int, int], str], start: Tuple[int, int], end: Tuple[int, int]) -> int:
    to_check = collections.deque([(*start, set())])
    cost_so_far = dict()
    cost_so_far[start] = 0

    while to_check:
        row_index, column_index, path = to_check.popleft()

        if (row_index, column_index) == end:
            continue

        for new_point in get_all_neighbors(hiking_map, (row_index, column_index)):
            new_cost = cost_so_far[row_index, column_index] + 1

            if new_point in path:
                continue

            if new_point not in cost_so_far or new_cost > cost_so_far[new_point]:
                cost_so_far[new_point] = new_cost

                new_path = path.copy()
                new_path.add(new_point)

                to_check.appendleft((*new_point, new_path))

    return cost_so_far[end]


def solution_for_first_part(task_input: Iterable[str]) -> int:
    hiking_map = parse(task_input)
    max_rows = max(row for row, _ in hiking_map.keys())
    start = next( point for point, tile in hiking_map.items() if point[0] == 0 and tile == '.' )
    end = next(point for point, tile in hiking_map.items() if point[0] == max_rows and tile == '.')

    return find_the_longest_path(get_neighbors_with_slops, hiking_map, start, end)


example_input = '''#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#'''.splitlines()


assert solution_for_first_part(example_input) == 94

# The input is taken from: https://adventofcode.com/2023/day/23/input
task_input = list(load_input_file('input.23.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def find_the_shortest_path_with_blockades(get_all_neighbors: Callable[[Dict[Tuple[int, int], str]], Iterable[Tuple[int, int]]], hiking_map: Dict[Tuple[int, int], str], start: Tuple[int, int], end: Tuple[int, int], blockades: Set[Tuple[int, int]]) -> int:
    to_check = [start]
    cost_so_far = dict()
    cost_so_far[start] = 0

    while to_check:
        column_index, row_index = to_check.pop()

        if (column_index, row_index) == end:
            return cost_so_far[end]

        if (column_index, row_index) != start and (column_index, row_index) in blockades:
            continue

        for new_point in get_all_neighbors(hiking_map, (column_index, row_index)):
            new_cost = cost_so_far[column_index, row_index] + 1

            if new_point not in cost_so_far or new_cost < cost_so_far[new_point]:
                cost_so_far[new_point] = new_cost
                to_check.append(new_point)


def build_graph(hiking_map, start: Dict[Tuple[int, int], str], end: Tuple[int, int]) -> Dict[Tuple[int, int], Dict[Tuple[int, int], int]]:
    crossings = [ start, end ]
    graph = { start: {} , end: {}  }

    for point in hiking_map:
        if hiking_map[point] == '#':
            continue

        if sum(1 for _ in get_all_neighbors(hiking_map, point)) > 2:
            crossings.append(point)
            graph[point] = {}

    for point in graph:
        for crossing in crossings:

            if crossing == point:
                continue

            if crossing in graph[point]:
                continue

            size = find_the_shortest_path_with_blockades(get_all_neighbors, hiking_map, point,  crossing, crossings)
            if size != None:
                graph[point][crossing] = size
                graph[crossing][point] = size

    return graph


def find_the_longest_path_by_graph(graph: Dict[Tuple[int, int], Dict[Tuple[int, int], int]], start: Tuple[int, int], end: Tuple[int, int]) -> int:
    to_check = [(start, 0, set() )]
    path_sizes = []

    while to_check:
        point, size, path = to_check.pop()
        if point == end:
            path_sizes.append(size)
            continue

        copy_path = path.copy()
        copy_path.add(point)

        for new_point in graph[point].keys():
            if new_point in path:
                continue

            to_check.append((new_point, size + graph[point][new_point], copy_path))

    return max(path_sizes)


def solution_for_second_part(task_input: Iterable[str]) -> int:
    hiking_map = parse(task_input)
    max_rows = max(row for row, _ in hiking_map.keys())

    start = next(point for point, tile in hiking_map.items() if point[0] == 0 and tile == '.' )
    end = next(point for point, tile in hiking_map.items() if point[0] == max_rows and tile == '.' )

    graph = build_graph(hiking_map, start, end)

    return find_the_longest_path_by_graph(graph, start, end)


assert solution_for_second_part(example_input) == 154

print("Solution for the second part:", solution_for_second_part(task_input))
