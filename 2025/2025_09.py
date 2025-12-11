from typing import Generator, Iterable, List, Tuple
import itertools


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[int, int], None, None]:
    for line in task_input:
        yield tuple(map(int, line.split(',')))


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return max(
        (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)
        for a, b in itertools.combinations(parse(task_input), 2))


example_input = '''7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3'''.splitlines()

assert solution_for_first_part(example_input) == 50
# The input is taken from: https://adventofcode.com/2025/day/9/input
task_input = list(load_input_file('input.09.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> int:

    def sort_edges(points: Iterable[Tuple[int, int]]) -> Tuple[List[Tuple[int, int, int]], List[Tuple[int, int, int]]]:
        next_point_iterator = iter(itertools.cycle(points))
        next(next_point_iterator)

        horizontal_edges = []
        vertical_edges = []
        for (x1, y1), (x2, y2) in zip(points, next_point_iterator):
            if x1 == x2:
                vertical_edges.append((x1, min(y1, y2), max(y1, y2)))
            elif y1 == y2:
                horizontal_edges.append((y1, min(x1, x2), max(x1, x2)))
            else:
                raise Exception('Unknown edge type')

        vertical_edges.sort()
        horizontal_edges.sort()

        return horizontal_edges, vertical_edges


    def check_horizontal_line(vertical_edges, y, x1, x2):
        for x, y1, y2 in vertical_edges:
            if  y1 <= y <= y2 and x1 <= x <= x2:
                return False

        return True


    def check_vertical_line(horizontal_edges, x, y1, y2):
        for y, x1, x2 in horizontal_edges:
            if  y1 <= y <= y2 and x1 <= x <= x2:
                return False

        return True


    def check_line(horizontal_edges, vertical_edges, x1, y1, x2, y2):
        if y1 == y2:
            return check_horizontal_line(vertical_edges, y1, min(x1, x2), max(x1, x2))
        elif x1 == x2:
            return check_vertical_line(horizontal_edges, x1, min(y1, y2), max(y1, y2))

        raise Exception('Unknown edge type')


    points = list(parse(task_input))
    horizontal_edges, vertical_edges = sort_edges(points)

    the_largest_area = 0
    for (x1, y1), (x2, y2) in itertools.combinations(points, 2):
        if x1 == x2 or y1 == y2:
            continue

        internal_x1, internal_x2 = min(x1, x2) + 1, max(x1, x2) - 1,
        internal_y1, internal_y2 = min(y1, y2) + 1, max(y1, y2) - 1,

        current_area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
        if current_area <= the_largest_area:
            continue

        if not (check_line(horizontal_edges, vertical_edges, internal_x1, internal_y1, internal_x1, internal_y2) \
            and check_line(horizontal_edges, vertical_edges, internal_x1, internal_y2, internal_x2, internal_y2) \
            and check_line(horizontal_edges, vertical_edges, internal_x2, internal_y2, internal_x2, internal_y1) \
            and check_line(horizontal_edges, vertical_edges, internal_x2, internal_y1, internal_x1, internal_y1)):
            continue

        the_largest_area = current_area

    return the_largest_area


assert solution_for_second_part(example_input) == 24
print("Solution for the second part:", solution_for_second_part(task_input))
