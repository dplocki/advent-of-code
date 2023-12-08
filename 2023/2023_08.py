from typing import Dict, Tuple
from itertools import cycle


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def parse(task_input: str) -> Tuple[str, Dict[str, str]]:
    instructions, raw_nodes_map = task_input.split('\n\n')

    nodes_map = {}
    for line in raw_nodes_map.splitlines():
        tokens = line.split(' = ')
        nodes_map[tokens[0]] = tokens[1][1:-1].split(', ')

    return instructions, nodes_map


def solution_for_first_part(task_input: str) -> int:
    instructions, nodes_map = list(parse(task_input))

    current = 'AAA'
    result = 0

    for instruction in cycle(instructions):
        node = nodes_map[current]

        if instruction == 'L':
            current = node[0]
        elif instruction == 'R':
            current = node[1]
        else:
            raise Exception(f'Unrecognized instruction: {instruction}')

        result += 1
        if current == 'ZZZ':
            return result


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
