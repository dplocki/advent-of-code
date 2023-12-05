from operator import itemgetter
from typing import Dict, List, Tuple


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def parse(task_input: str) -> Dict[str, Tuple[int]]:
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
        result[name] = sorted(
            (tuple(map(int, line.split())) for line in segment[1:]),
            key=itemgetter(1)
        )

    return result


def transform_single_value_by_almanac(value, chapter: List[Tuple[int, int, int]]) -> int:
    for destination, source, length in chapter:
        if source <= value <= source + length:
            return destination + (value - source)

    return value


def solution_for_first_part(task_input: str) -> int:
    almanac = parse(task_input)

    locations = []
    for value in almanac['seeds']:
        for name in almanac['order']:
            value = transform_single_value_by_almanac(value, almanac[name])

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


def is_intersection(range_a: Tuple[int, int], range_b: Tuple[int, int]) -> bool:
    return not (range_b[0] + range_b[1] < range_a[0] or range_a[0] + range_a[1] < range_b[0])


def find_in_almanac(value_ranges: Tuple[int, int], chapter: List[Tuple[int, int, int]]) -> int:
    result = []

    for destination, source, length in chapter:
        new_value_ranges = []
        for value_range in value_ranges:
            if is_intersection(value_range, (source, length)):
                intersection_begin = max(value_range[0], source)
                intersection_end = min(value_range[0] + value_range[1], source + length)

                result.append((destination + intersection_begin - source, intersection_end - intersection_begin))

                if value_range[0] < intersection_begin:
                    result.append((value_range[0], intersection_begin - value_range[0]))

                if (value_range[0] + value_range[1]) > intersection_end:
                    new_value_ranges.append((intersection_end, value_range[0] + value_range[1] - intersection_end))
            else:
                new_value_ranges.append(value_range)

        value_ranges = new_value_ranges

    result.extend(value_ranges)
    return result


def solution_for_second_part(task_input: str) -> int:
    almanac = parse(task_input)
    value_ranges = zip(almanac['seeds'][::2], almanac['seeds'][1::2])
    for name in almanac['order']:
        value_ranges = find_in_almanac(value_ranges, almanac[name])

    return min(value_range[0] for value_range in value_ranges)


assert solution_for_second_part(example_input) == 46
print("Solution for the second part:", solution_for_second_part(task_input))