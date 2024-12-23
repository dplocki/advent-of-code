from typing import Generator, Iterable, Tuple
import itertools


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[str, str], None, None]:
    for line in task_input:
        yield tuple(line.split('-'))


def solution_for_first_part(task_input: Iterable[str]) -> int:
    connections = set()
    computers = set()

    for first_computer, second_computer in parse(task_input):
        connections.add((first_computer, second_computer))
        connections.add((second_computer, first_computer))
        computers.add(first_computer)
        computers.add(second_computer)


    result = 0
    for first_computer, second_computer, third_computer in itertools.combinations(computers, 3):
        if not (first_computer.startswith('t') or second_computer.startswith('t') or third_computer.startswith('t')):
            continue

        if (first_computer, second_computer) not in connections:
            continue

        if (second_computer, third_computer) not in connections:
            continue

        if (first_computer, third_computer) not in connections:
            continue

        result += 1

    return result


example_input = '''kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn'''.splitlines()

assert solution_for_first_part(example_input) == 7

# The input is taken from: https://adventofcode.com/2024/day/23/input
task_input = list(load_input_file('input.23.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
