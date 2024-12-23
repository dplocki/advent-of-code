from collections import defaultdict
from typing import Dict, Generator, Iterable, Set, Tuple
import itertools


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Tuple[Set[Tuple[str, str]], Set[str]]:
    connections = defaultdict(set)

    for line in task_input:
        first_computer, second_computer = line.split('-')

        connections[first_computer].add(second_computer)
        connections[second_computer].add(first_computer)

    return connections


def solution_for_first_part(task_input: Iterable[str]) -> int:
    connections = parse(task_input)
    result = 0

    for first_computer, second_computer, third_computer in itertools.combinations(connections.keys(), 3):
        if not (first_computer.startswith('t') or second_computer.startswith('t') or third_computer.startswith('t')):
            continue

        if second_computer not in connections[first_computer]:
            continue

        if third_computer not in connections[first_computer]:
            continue

        if second_computer not in connections[third_computer]:
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


def bron_kerbosch_all_cliques(current_clique: Set[str], nodes_to_checked: Set[str], checked_nodes: Set[str], graph: Dict[str, Set[str]]):
    yield current_clique
    for v in list(nodes_to_checked):
        yield from bron_kerbosch_all_cliques(
                current_clique.union({v}),
                nodes_to_checked.intersection(graph[v]),
                checked_nodes.intersection(graph[v]),
                graph,
            )

        nodes_to_checked.remove(v)
        checked_nodes.add(v)


def solution_for_second_part(task_input: Iterable[str]) -> str:
    connections = parse(task_input)

    groups = list(bron_kerbosch_all_cliques(set(), set(connections.keys()), set(), connections))

    the_largest_group = max(groups, key=lambda g: len(g))
    return ','.join(sorted(the_largest_group))


assert solution_for_second_part(example_input) == 'co,de,ka,ta'
print("Solution for the second part:", solution_for_second_part(task_input))
