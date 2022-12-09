from typing import Generator, Iterable, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[str, int], None, None]:
    for line in task_input:
        tokens = line.split(' ')
        yield tokens[0], int(tokens[1])


def update_tail(tail: Tuple[int, int], head: Tuple[int, int], previous_head: Tuple[int, int]) -> Tuple[int, int]:
    diff_x = head[0] - tail[0]
    diff_y = head[1] - tail[1]

    if abs(diff_x) <= 1 and abs(diff_y) <= 1:
        return tail

    return previous_head


def solution_for_first_part(task_input: Iterable[str]) -> int:
    directory_table = {
        'R': (1, 0),
        'L': (-1, 0),
        'U': (0, 1),
        'D': (0, -1)
    }

    visited = set()
    prev_head = (0, 0)
    head = (0, 0)
    tail = (0, 0)

    for where, much_long in parse(task_input):
        dir = directory_table[where]

        for _ in range(much_long):
            prev_head = head
            head = head[0] + dir[0], head[1] + dir[1]
            tail = update_tail(tail, head, prev_head)
            visited.add(tail)

    return len(visited)


example_input = '''R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2'''.splitlines()

assert solution_for_first_part(example_input) == 13

# The input is taken from: https://adventofcode.com/2022/day/9/input
task_input = list(load_input_file('input.09.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
