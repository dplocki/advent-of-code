from operator import mul
from typing import Callable, Dict, Generator, Iterable, Set, Tuple


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


def get_region_size_and_fence_length(garden_map: Dict[Tuple[int, int], str], locations_measured: Set[Tuple[int, int]], location: Tuple[int, int]) -> Tuple[int, int]:
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


def solution(get_region_price: Callable[[Dict[Tuple[int, int], str], Set[Tuple[int, int]], Tuple[int, int]], Tuple[int, int]], task_input: Iterable[str]) -> int:
    garden_map = parse(task_input)
    locations_measured = set()

    return sum(
        mul(*get_region_price(garden_map, locations_measured, location))
        for location in garden_map
        if location not in locations_measured)


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return solution(get_region_size_and_fence_length, task_input)


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


def get_region_size_and_sides(garden_map: Dict[Tuple[int, int], str], locations_measured: Set[Tuple[int, int]], location: Tuple[int, int]) -> Tuple[int, int]:
    region = garden_map[location]
    to_check = [location]
    size = 0
    sides = 0

    while to_check:
        current = to_check.pop()
        if garden_map[current] != region:
            continue

        if current in locations_measured:
            continue

        locations_measured.add(current)

        size += 1

        if garden_map.get((current[0] - 1, current[1]), None) == region and garden_map.get((current[0], current[1] - 1), None) == region and garden_map.get((current[0] - 1, current[1] - 1), None) != region:
            sides += 1

        if garden_map.get((current[0] - 1, current[1]), None) != region and garden_map.get((current[0], current[1] - 1), None) != region:
            sides += 1

        if garden_map.get((current[0] - 1, current[1]), None) == region and garden_map.get((current[0], current[1] + 1), None) == region and garden_map.get((current[0] - 1, current[1] + 1), None) != region:
            sides += 1

        if garden_map.get((current[0] - 1, current[1]), None) != region and garden_map.get((current[0], current[1] + 1), None) != region:
            sides += 1

        if garden_map.get((current[0] + 1, current[1]), None) == region and garden_map.get((current[0], current[1] - 1), None) == region and garden_map.get((current[0] + 1, current[1] - 1), None) != region:
            sides += 1

        if garden_map.get((current[0] + 1, current[1]), None) != region and garden_map.get((current[0], current[1] - 1), None) != region:
            sides += 1

        if garden_map.get((current[0] + 1, current[1]), None) == region and garden_map.get((current[0], current[1] + 1), None) == region and garden_map.get((current[0] + 1, current[1] + 1), None) != region:
            sides += 1

        if garden_map.get((current[0] + 1, current[1]), None) != region and garden_map.get((current[0], current[1] + 1), None) != region:
            sides += 1

        for neighbor in ((0, -1), (1, 0), (-1, 0), (0, 1)):
            new_location = (current[0] + neighbor[0], current[1] + neighbor[1])
            value = garden_map.get(new_location, None)
            if value != None:
                to_check.append(new_location)

    return size, sides


def solution_for_second_part(task_input: Iterable[str]) -> int:
    return solution(get_region_size_and_sides, task_input)


assert solution_for_second_part(example_input) == 1206

assert solution_for_second_part('''AAAA
BBCD
BBCC
EEEC'''.splitlines()) == 80

assert solution_for_second_part('''EEEEE
EXXXX
EEEEE
EXXXX
EEEEE'''.splitlines()) == 236

assert solution_for_second_part('''AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA'''.splitlines()) == 368

print("Solution for the second part:", solution_for_second_part(task_input))
