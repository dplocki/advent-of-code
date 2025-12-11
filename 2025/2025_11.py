from typing import Callable, Dict, Generator, Iterable, Tuple
from functools import cache


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Dict[str, Tuple[str, ...]]:
    result = {}
    for line in task_input:
        start, nodes = line.split(': ')
        result[start] = tuple(nodes.split(' '))

    return result


def count_paths(node_map: Dict[str, Tuple[str, ...]]) -> Callable[[str, str], int]:

    @cache
    def internal(start: str, end: str) -> int:
        if start == end:
            return 1

        if start == 'out':
            return 0

        return sum(
            internal(node, end)
            for node in node_map[start]
        )

    return internal


def solution_for_first_part(task_input: Iterable[str]) -> int:
    node_map = parse(task_input)
    return count_paths(node_map)('you', 'out')


example_input_part_1 = '''aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
'''.splitlines()

assert solution_for_first_part(example_input_part_1) == 5
# The input is taken from: https://adventofcode.com/2025/day/11/input
task_input = list(load_input_file('input.11.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> int:
    node_map = parse(task_input)
    counter = count_paths(node_map)

    return (
        counter('svr', 'fft') * counter('fft', 'dac') * counter('dac', 'out')
        + counter('svr', 'dac') * counter('dac', 'fft') * counter('fft', 'out')
    )


example_input_part_2 = '''svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
'''.splitlines()

assert solution_for_second_part(example_input_part_2) == 2
print("Solution for the second part:", solution_for_second_part(task_input))
