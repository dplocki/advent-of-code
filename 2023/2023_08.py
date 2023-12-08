from math import lcm
from typing import Dict, Generator, Tuple
from itertools import cycle, takewhile


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def parse(task_input: str) -> Tuple[str, Dict[str, Tuple[str, str]]]:
    instructions, raw_nodes_map = task_input.split('\n\n')

    nodes_map = {}
    for line in raw_nodes_map.splitlines():
        tokens = line.split(' = ')
        nodes_map[tokens[0]] = tokens[1][1:-1].split(', ')

    return instructions, nodes_map


def walk(instructions: str, nodes_map: Dict[str, Tuple[str, str]], start_node: str) -> Generator[str, None, None]:
    current = start_node

    for instruction in cycle(instructions):
        node = nodes_map[current]

        if instruction == 'L':
            current = node[0]
        elif instruction == 'R':
            current = node[1]
        else:
            raise Exception(f'Unrecognized instruction: {instruction}')

        yield current


def solution_for_first_part(task_input: str) -> int:
    instructions, nodes_map = parse(task_input)
    return sum(1 for _ in takewhile(lambda node: node != 'ZZZ', walk(instructions, nodes_map, 'AAA'))) + 1


assert solution_for_first_part('''RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)''') == 2

assert solution_for_first_part('''LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
''') == 6

# The input is taken from: https://adventofcode.com/2023/day/8/input
task_input = load_input_file('input.08.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: str) -> int:
    instructions, nodes_map = parse(task_input)
    end_predicate = lambda node: node[-1] != 'Z'
    start_nodes = [node for node in nodes_map.keys() if node[-1] == 'A']
    cycles_counter = [
        sum(1 for _ in takewhile(end_predicate, walk(instructions, nodes_map, node))) + 1
        for node in start_nodes
    ]

    return lcm(*cycles_counter)


assert solution_for_second_part('''LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)''') == 6

print("Solution for the second part:", solution_for_second_part(task_input))
