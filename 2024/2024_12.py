from typing import Dict, Generator, Iterable, Set, Tuple


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Dict[Tuple[int, int], str]:
    return {(row, column): character
        for row, line in enumerate(task_input)
        for column, character in enumerate(line)}


def get_region(garden_map: Dict[Tuple[int, int], str], locations_measured: Set[Tuple[int, int]], location: Tuple[int, int]) -> Tuple[int, int]:
    region = garden_map[location]
    size = 0
    fence = 0
    to_check = [location]

    while to_check:
        current = to_check.pop()
        if garden_map[current] != region or current in locations_measured:
            continue

        locations_measured.add(current)
        size += 1

        for neighbor in ((0, -1), (1, 0), (-1, 0), (0, 1)):
            new_location = (current[0] + neighbor[0], current[1] + neighbor[1])
            value = garden_map.get(new_location, None)
            if value != region:
                fence += 1
            elif value != None:
                to_check.append(new_location)

    return size, fence


def solution_for_first_part(task_input: Iterable[str]) -> int:
    garden_map = parse(task_input)
    locations_measured = set()
    result = 0

    for location in garden_map:
        if location in locations_measured:
            continue

        size, fence = get_region(garden_map, locations_measured, location)
        result += size * fence

    return result


example_input = '''RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE'''.splitlines()

assert solution_for_first_part(example_input) == 1930

# The input is taken from: https://adventofcode.com/2024/day/12/input
task_input = list(load_input_file('input.12.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
