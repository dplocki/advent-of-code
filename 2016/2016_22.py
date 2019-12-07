import itertools
import re


X = 0
Y = 1
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


def build_node_map(nodes):
    return {(x, y):(used, avail) for x, y, _, used, avail, _ in nodes}


def find_avaible_neighbors(nodes_map):
    for x, y in nodes_map.keys():
        check = lambda _x, _y: (_x, _y) in nodes_map and nodes_map[(_x, _y)][1] >= nodes_map[(x, y)][0]

        if check(x + 1, y) and check(x - 1, y) and check(x, y + 1) and check(x, y - 1):
            yield x, y


def visualization(nodes):
    USED = 0
    AVAIL = 1

    nodes_map = build_node_map(nodes)
    max_x = sorted(nodes, key=lambda n: n[X], reverse=True)[0][X]
    max_y = sorted(nodes, key=lambda n: n[Y], reverse=True)[0][Y]
    empty_node = next(find_avaible_neighbors(nodes_map))

    result = '|' + '|'.join([str(x) for x in range(max_x + 1)]) + '|\n|' + '|'.join(['-' * 5 for x in range(max_x + 1)]) + '|\n'
    for y in range(max_y + 1):
        result += '|'
        for x in range(max_x + 1):
            tmp = f'{x}:{y}'

            if (x, y) == empty_node:
                tmp = 'EMPTY ' + tmp

            if nodes_map[(x, y)][USED] > nodes_map[empty_node][AVAIL]:
                tmp = '**' + tmp + '**'

            result += tmp + '|'
        
        result += '\n'

    return result


with open('visualisation.2016.22.md', 'w') as file:
    file.write(visualization(nodes))

# Solution for second part:
# Calculated by "hand" -> moving empty node into data node (on begin: max_x, 0)
# then start pushing it into top left cornert (5 moves of empty node per each step)
