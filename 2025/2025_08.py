from typing import Counter, Generator, Iterable, Tuple
from functools import reduce
import itertools
import operator


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[int, int, int], None, None]:
    for line in task_input:
        yield tuple(map(int, line.split(',')))


def joining_boxes(task_input: Iterable[str]):
    boxes = list(parse(task_input))
    distances = [
        (sum(((a[i] - b[i]) ** 2) for i in range(3)), a, b)
        for a, b in itertools.combinations(boxes, 2)
    ]
    distances.sort()
    group_map = { box: index for index, box in enumerate(boxes) }

    for (_, box1, box2) in distances:
        new_index = group_map[box2]
        for key in group_map:
            if group_map[key] == new_index:
                group_map[key] = group_map[box1]

        yield box1, box2, group_map


def solution_for_first_part(task_input: Iterable[str], how_much=1_000) -> int:
    for (_, _, group_map), _ in zip(joining_boxes(task_input), range(how_much - 1)):
        pass

    return reduce(
            operator.mul,
            map(operator.itemgetter(1), Counter(group_map.values()).most_common(3)),
            1
        )


example_input = '''162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689'''.splitlines()

assert solution_for_first_part(example_input, 10) == 40
# The input is taken from: https://adventofcode.com/2025/day/8/input
task_input = list(load_input_file('input.08.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> int:
    for box1, box2, group_map in joining_boxes(task_input):
        if (len(set(group_map.values()))) == 1:
            return box1[0] * box2[0]

    raise Exception('Unknown state')


assert solution_for_second_part(example_input) == 25272
print("Solution for the second part:", solution_for_second_part(task_input))
