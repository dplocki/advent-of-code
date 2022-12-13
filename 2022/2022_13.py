from functools import cmp_to_key
from itertools import chain
from typing import Generator, Iterable, List, Tuple, Union


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def parse(task_input: Iterable[str]) -> Generator[Tuple[List, List], None, None]:
    for lines in task_input.split('\n\n'):
        left, right = lines.splitlines()
        yield eval(left), eval(right)


def are_correct_order(left: Union[int, List], right: Union[int, List]) -> int:
    if type(left) is int and type(right) is int:
        return -1 if left < right else 0 if left == right else 1

    if type(left) is list and type(right) is int:
        return are_correct_order(left, [right])

    if type(right) is list and type(left) is int:
        return are_correct_order([left], right)

    index = 0
    while True:
        if index >= len(right) and index < len(left):
            return 1

        if index >= len(left) and index < len(right):
            return -1

        if index >= len(left):
            return 0

        order = are_correct_order(left[index], right[index])
        if order != 0:
            return order

        index += 1


def solution_for_first_part(task_input: Iterable[str]) -> int:
    pairs = parse(task_input)

    return sum(
        index + 1
        for index, pair in enumerate(pairs)
        if are_correct_order(pair[0], pair[1]) != 1)


example_input = '''[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]'''

assert solution_for_first_part(example_input) == 13

# The input is taken from: https://adventofcode.com/2022/day/13/input
task_input = load_input_file('input.13.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> int:
    ADDITIONAL_PACKETS = [
        [[2]],
        [[6]]
    ]

    pairs = parse(task_input)
    packets = list(chain(*pairs))
    packets.extend(ADDITIONAL_PACKETS)

    packets.sort(key=cmp_to_key(are_correct_order))

    result = 1
    for packet in ADDITIONAL_PACKETS:
        result *= packets.index(packet) + 1

    return result


assert solution_for_second_part(example_input) == 140
print("Solution for the second part:", solution_for_second_part(task_input))
