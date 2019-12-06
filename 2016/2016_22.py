import itertools
import re


USED = 3
AVAIL = 4


def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(lines):
    pattern = re.compile(r'\/dev\/grid\/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%')
    group_numbers = list(range(1, 7))

    for line in lines:
        groups = pattern.match(line)
        if groups:
            yield [int(groups[i]) for i in group_numbers]


def solution_for_first_part(nodes):
    return sum([
            1
            for node_a, node_b in itertools.permutations(nodes, 2)
            if node_a[USED] != 0 and node_a[USED] <= node_b[AVAIL]
        ])


# The input is taken from: https://adventofcode.com/2016/day/22/input
nodes = list(parse(load_input_file('input.22.txt')))
print("Solution for the first part:", solution_for_first_part(nodes))
