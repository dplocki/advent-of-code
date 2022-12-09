from typing import Generator, Iterable, List, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[str, int], None, None]:
    for line in task_input:
        tokens = line.split(' ')
        yield tokens[0], int(tokens[1])


def sign(number: int) -> int:
    return (number > 0) - (number < 0)


def update_knot(tail: Tuple[int, int], head: Tuple[int, int]) -> Tuple[int, int]:
    diff_x = head[0] - tail[0]
    diff_y = head[1] - tail[1]

    if abs(diff_x) <= 1 and abs(diff_y) <= 1:
        return tail

    return tail[0] + sign(diff_x), tail[1] + sign(diff_y)


def update_rope(rope: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    for i in range(1, len(rope)):
        rope[i] = update_knot(rope[i], rope[i - 1])

    return rope


def solution(knots_number: int, task_input: Iterable[str]) -> int:
    directory_table = {
        'R': (1, 0),
        'L': (-1, 0),
        'U': (0, 1),
        'D': (0, -1)
    }

    visited = set()
    rope = [(0, 0)] * knots_number

    for where, much_long in parse(task_input):
        dir = directory_table[where]
        for _ in range(much_long):
            rope[0] = rope[0][0] + dir[0], rope[0][1] + dir[1]
            rope = update_rope(rope)
            visited.add(rope[-1])

    return len(visited)


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return solution(2, task_input)


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

example_input_larger = '''R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20'''.splitlines()


def solution_for_second_part(task_input: Iterable[str]) -> int:
    return solution(10, task_input)


assert solution_for_second_part(example_input) == 1
assert solution_for_second_part(example_input_larger) == 36

print("Solution for the second part:", solution_for_second_part(task_input))
