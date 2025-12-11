from typing import Dict, Generator, Iterable, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Dict[str, Tuple[str, ...]]:
    result = {}
    for line in task_input:
        start, nodes = line.split(': ')
        result[start] = tuple(nodes.split(' '))

    return result


def solution_for_first_part(task_input: Iterable[str]) -> int:
    node_map = parse(task_input)
    result = 0
    to_check = ['you']

    while to_check:
        current_node = to_check.pop()
        if current_node == 'out':
            result += 1
            continue

        for node in node_map[current_node]:
            to_check.append(node)

    return result


example_input = '''aaa: you hhh
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

assert solution_for_first_part(example_input) == 5
# The input is taken from: https://adventofcode.com/2025/day/11/input
task_input = list(load_input_file('input.11.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
