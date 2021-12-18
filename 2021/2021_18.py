import functools
from itertools import permutations
import math
from typing import Any


MAXIMUM_DEPT = 5
MAXIMUM_VALUE = 10


def load_input_file(file_name: str) -> list[str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(line: str) -> list[tuple[int, int]]:
    current_level = 0
    for character in line:
        if character == '[':
            current_level += 1
        elif character == ']':
            current_level -= 1
        elif character in '0123456789':
            yield int(character), current_level

    assert current_level == 0


def str_to_snailfish_number(line: str) -> list[tuple[int, int]]:
    return list(parse(line))


def find_first_match(match: callable, colletion: list[Any]) -> tuple[int, Any]:
    for index, element in enumerate(colletion):
        if match(element):
            return index, element

    return -1, None


def explode(elements: list[tuple[int, int]]) -> tuple[list[tuple[int, int]], bool]:
    index, element = find_first_match(lambda element: element[1] == MAXIMUM_DEPT, elements)
    if not element:
        return elements, False

    elements_number = len(elements)
    left_part = elements[:index] if index > 0 else []
    rigth_part = elements[index + 2:] if index + 2 < elements_number else []

    if index > 0:
        left_part[-1] = (left_part[-1][0] + element[0], left_part[-1][1])

    if index + 2 < elements_number:
        rigth_part[0] = (rigth_part[0][0] + elements[index + 1][0], rigth_part[0][1])

    return left_part + [(0, MAXIMUM_DEPT - 1)] + rigth_part, True


def split(elements: list[tuple[int, int]]) -> tuple[list[tuple[int, int]], bool]:
    index, element = find_first_match(lambda element: element[0] >= MAXIMUM_VALUE, elements)
    if not element:
        return elements, False

    return elements[:index] + [(math.floor(element[0] / 2), element[1] + 1), (math.ceil(element[0] / 2), element[1] + 1)] + elements[index + 1:], True


def snailfish_sum(first: list[tuple[int, int]], second: list[tuple[int, int]]) -> list[tuple[int, int]]:

    def raise_level(elements):
        return ((element[0], element[1] + 1) for element in elements)


    result = list(raise_level(first)) + list(raise_level(second))
    while True:
        result, changed = explode(result)
        if changed == True:
            continue

        result, changed = split(result)
        if changed == True:
            continue

        break

    return result


def calculate_magnitute(snailfish_number: list[tuple[int, int]]) -> int:

    def magni_red(elements, level):
        index, element = find_first_match(lambda element: element[1] >= level, elements)
        if not element:
            return elements, False

        return elements[:index] + [(elements[index][0] *  3 + 2 * elements[index + 1][0], elements[index][1] - 1)] + elements[index + 2:], True


    for level in range(MAXIMUM_DEPT - 1, 0, -1):
        run = True
        while run:
            snailfish_number, run = magni_red(snailfish_number, level)

    return snailfish_number[0][0]


def solution_for_first_part(task_input: list[str]) -> int:
    snailfish_numbers = list(map(lambda line: list(parse(line)), task_input))
    result = functools.reduce(snailfish_sum, snailfish_numbers)
    
    return calculate_magnitute(result)


assert explode(str_to_snailfish_number('[[[[[9,8],1],2],3],4]'))[0] == str_to_snailfish_number('[[[[0,9],2],3],4]')
assert explode(str_to_snailfish_number('[7,[6,[5,[4,[3,2]]]]]'))[0] == str_to_snailfish_number('[7,[6,[5,[7,0]]]]')
assert explode(str_to_snailfish_number('[[6,[5,[4,[3,2]]]],1]'))[0] == str_to_snailfish_number('[[6,[5,[7,0]]],3]')
assert explode(str_to_snailfish_number('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]'))[0] == str_to_snailfish_number('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
assert explode(str_to_snailfish_number('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'))[0] == str_to_snailfish_number('[[3,[2,[8,0]]],[9,[5,[7,0]]]]')

assert split([(0, 4), (7, 4), (4, 3), (15, 3), (0, 4), (1, 4), (3, 4), (1, 2), (1, 2)])[0] == str_to_snailfish_number('[[[[0,7],4],[[7,8],[0,13]]],[1,1]]')

assert calculate_magnitute(str_to_snailfish_number('[[1,2],[[3,4],5]]')) == 143
assert calculate_magnitute(str_to_snailfish_number('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')) == 1384
assert calculate_magnitute(str_to_snailfish_number('[[[[1,1],[2,2]],[3,3]],[4,4]]')) == 445
assert calculate_magnitute(str_to_snailfish_number('[[[[3,0],[5,3]],[4,4]],[5,5]]')) == 791
assert calculate_magnitute(str_to_snailfish_number('[[[[5,0],[7,4]],[5,5]],[6,6]]')) == 1137
assert calculate_magnitute(str_to_snailfish_number('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]')) == 3488


example_input = '''[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'''.splitlines()


assert solution_for_first_part(example_input) == 4140

# The input is taken from: https://adventofcode.com/2021/day/18/input
task_input = list(load_input_file('input.18.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input):
    snailfish_numbers = list(map(lambda line: list(parse(line)), task_input))

    return max(calculate_magnitute(snailfish_sum(a, b)) for a, b in permutations(snailfish_numbers, 2))


assert solution_for_second_part(example_input) == 3993
print("Solution for the second part:", solution_for_second_part(task_input))
