from typing import Generator, Iterable, List, Set, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Tuple[int, List[Set[int]]]:
    result = []
    start = None
    for line in task_input:
        splitter = set()
        for column, character in enumerate(line):
            if character == 'S':
                start = column
            elif character == '^':
                splitter.add(column)

        result.append(splitter)

    return start, result


def solution_for_first_part(task_input: Iterable[str]) -> int:
    start, splitters = parse(task_input)
    rays = { start: True }
    result = 0

    for splitter in splitters:
        new_rays = {}

        for column, is_ray in rays.items():
            if not is_ray:
                continue

            if column in splitter:
                new_rays[column - 1] = True
                new_rays[column + 1] = True
                new_rays[column] = False
                result += 1
            else:
                new_rays[column] = True

        rays = new_rays

    return result


example_input = '''.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............'''.splitlines()

assert solution_for_first_part(example_input) == 21
# The input is taken from: https://adventofcode.com/2025/day/7/input
task_input = list(load_input_file('input.07.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> int:
    start, splitters = parse(task_input)
    timelines = { start: 1 }

    for splitter in splitters:
        for s in splitter:
            timelines[s - 1] = timelines.get(s - 1, 0) + timelines[s]
            timelines[s + 1] = timelines.get(s + 1, 0) + timelines[s]
            timelines[s] = 0

    return  sum(timelines.values())


assert solution_for_second_part(example_input) == 40
print("Solution for the second part:", solution_for_second_part(task_input))
