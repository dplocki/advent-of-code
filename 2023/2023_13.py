from typing import Callable, Generator, Iterable, List, Set, Tuple


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def parse(task_input: str) -> Generator[Set[Tuple[int, int]], None, None]:
    for shape in task_input.split('\n\n'):
        yield set(
            (row_index, column_index)
            for row_index, row in enumerate(shape.splitlines())
            for column_index, character in enumerate(row)
            if character == '#')


def is_reflection(line_to_compeer: List[Set[int]], start: int) -> bool:
    return all(a == b for a, b in zip(line_to_compeer[start::-1], line_to_compeer[start+1:]))


def find_column_with_mirror(is_reflection: Callable[[List[Set[int]], int], bool], shape: Set[Tuple[int, int]]) -> int:
    star = next(iter(shape))
    maximum_row, maximum_column = star

    for row, column in shape:
        maximum_column = max(column, maximum_column)
        maximum_row = max(row, maximum_row)

    rows = [set(column for row, column in shape if row == index)
            for index in range(0, maximum_row + 1)]

    for index in range(0, maximum_row):
        if is_reflection(rows, index):
            return (index + 1) * 100

    columns = [set(row for row, column in shape if column == index)
               for index in range(0, maximum_column + 1)]

    for index in range(0, maximum_column):
        if is_reflection(columns, index):
            return index + 1

    raise Exception('not found')


def solution(is_reflection: Callable[[List[Set[int]], int], bool], task_input: Iterable[str]) -> int:
    shapes = list(parse(task_input))

    return sum(
        find_column_with_mirror(is_reflection, shape)
        for shape in shapes
    )


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return solution(is_reflection, task_input)


example_input = '''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''

assert solution_for_first_part(example_input) == 405

# The input is taken from: https://adventofcode.com/2023/day/13/input
task_input = load_input_file('input.13.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


def is_reflection_with_smudge(line_to_compeer: List[Set[int]], start: int) -> bool:
    smudges = sum(len(a ^ b) for a, b in zip(line_to_compeer[start::-1], line_to_compeer[start+1:]))
    return smudges == 1


def solution_for_second_part(task_input: Iterable[str]) -> int:
    return solution(is_reflection_with_smudge, task_input)


assert solution_for_second_part(example_input) == 400
print("Solution for the second part:", solution_for_second_part(task_input))
