import re


def file_to_input_list(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def parse_lines(lines):
    pattern = re.compile(r'^\#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$')
    for line in lines:
        match = pattern.match(line)
        yield int(match[2]), int(match[3]), int(match[4]), int(match[5])


def aplay(fabric_size: int, cuts: []):
    fabric = [0] * (fabric_size ** 2)

    for cut in cuts:
        for x in range(cut[2]):
            for y in range(cut[3]):
                fabric[(cut[1] + y)*fabric_size + cut[0] + x] += 1

    return fabric


def count_overlaps_for_fabric_and_cuts(fabric_size: int, cuts: []) -> int:
    fabric = aplay(fabric_size, parse_lines(cuts))

    return sum(f > 1 for f in fabric)

test_input = ['#1 @ 1,3: 4x4', '#2 @ 3,1: 4x4', '#3 @ 5,5: 2x2']

assert count_overlaps_for_fabric_and_cuts(8, test_input) == 4

print("Solution for first part:", count_overlaps_for_fabric_and_cuts(1000, file_to_input_list('input.03.txt')))
