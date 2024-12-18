import heapq
from typing import Dict, Generator, Iterable, Tuple


NEIGHBORS = ((0, -1), (1, 0), (-1, 0), (0, 1))


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[int, int], None, None]:
    for line in task_input:
        yield tuple(map(int, line.split(',')))


def heuristic(point_from: Tuple[int, int], point_to: Tuple[int, int]) -> int:
    return abs(point_from[0] - point_to[0]) + abs(point_from[1] - point_to[1])


def find_path(memory_map: Dict[Tuple[int, int], str], start: Tuple[int, int], end: Tuple[int, int]) -> int:
    to_check = []
    visited = { start: 0 }

    heapq.heappush(to_check, (0, 0, start))

    while to_check:
        priority, steps_count, current = heapq.heappop(to_check)
        if current == end:
            return steps_count

        next_point_steps_count = steps_count + 1
        for neighbor in NEIGHBORS:
            next_point = current[0] + neighbor[0], current[1] + neighbor[1]
            if next_point not in memory_map or memory_map[next_point] == '#':
                continue

            if next_point not in visited or next_point_steps_count < visited[next_point]:
                visited[next_point] = next_point_steps_count
                priority = next_point_steps_count + heuristic(next_point, end)
                heapq.heappush(to_check, (priority, next_point_steps_count, next_point))

    return None


def solution_for_first_part(task_input: Iterable[str], memory_map_size: int, first_elements_count: int) -> int:
    memory_map = {
        (x, y): '.'
        for x in range(memory_map_size)
        for y in range(memory_map_size)
    }

    for (x, y), _ in zip(parse(task_input), range(first_elements_count)):
        memory_map[x, y] = '#'

    start = (0, 0)
    end = (memory_map_size - 1, memory_map_size - 1)

    return find_path(memory_map, start, end)


example_input = '''5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0'''.splitlines()

assert solution_for_first_part(example_input, 7, 12) == 22

# The input is taken from: https://adventofcode.com/2024/day/18/input
task_input = list(load_input_file('input.18.txt'))
print("Solution for the first part:", solution_for_first_part(task_input, 71, 1024))


def solution_for_second_part(task_input: Iterable[str], memory_map_size: int, first_elements_count: int) -> int:
    memory_map = {
        (x, y): '.'
        for x in range(memory_map_size)
        for y in range(memory_map_size)
    }

    broken_bytes_generator = parse(task_input)

    for (x, y), _ in zip(broken_bytes_generator, range(first_elements_count)):
        memory_map[x, y] = '#'

    start = (0, 0)
    end = (memory_map_size - 1, memory_map_size - 1)

    for (x, y) in broken_bytes_generator:
        memory_map[x, y] = '#'

        if find_path(memory_map, start, end) == None:
            return f'{x},{y}'

    raise Exception('No solution')


assert solution_for_second_part(example_input, 7, 12) == '6,1'
print("Solution for the second part:", solution_for_second_part(task_input, 71, 1024))
