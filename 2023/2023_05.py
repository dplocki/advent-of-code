from typing import Dict, Iterable, Tuple


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def parse(task_input: Iterable[str]) -> Dict[str, Tuple[int]]:
    source = task_input.split('\n\n')
    seeds_seg = source[0]
    seeds = tuple(map(int, seeds_seg.split(':')[1].split()))
    result = {
        'seeds': seeds,
        'order': []
    }

    for segment in source[1:]:
        segment = segment.splitlines()
        name = segment[0].split(' ')[0]
        result['order'].append(name)
        result[name] = [
            tuple(map(int, line.split()))
            for line in segment[1:]
        ]

    return result


def find_in_almanac(value, chapter):
    for destination, source, length in chapter:
        if source <= value <= source + length:
            return destination + (value - source)

    return value


def solution_for_first_part(task_input: Iterable[str]) -> int:
    almanac = parse(task_input)

    locations = []
    for value in almanac['seeds']:
        for name in almanac['order']:
            value = find_in_almanac(value, almanac[name])

        locations.append(value)

    return min(locations)


example_input = '''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4'''

assert solution_for_first_part(example_input) == 35

# The input is taken from: https://adventofcode.com/2023/day/5/input
task_input = load_input_file('input.05.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
