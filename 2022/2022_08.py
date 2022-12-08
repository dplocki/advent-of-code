from typing import Dict, Generator, Iterator, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterator[str]) -> Generator[str, None, None]:
    for row_index, line in enumerate(task_input):
        for column_index, character in enumerate(line):
            yield row_index, column_index, int(character)


def build_tree_map(task_input: Iterator[str]) -> Tuple[int, int, Dict[Tuple[int, int], int]]:
    max_row, max_column, tree_map = 0, 0, {}
    for row_index, column_index, tree_hight in parse(task_input):
        tree_map[row_index, column_index] = tree_hight
        max_column = max(column_index, max_column)
        max_row = max(row_index, max_row)

    return max_row, max_column, tree_map


def solution_for_first_part(task_input: Iterator[str]) -> int:
    max_row, max_column, tree_map = build_tree_map(task_input)

    result = set()
    for row in range(1, max_row):
        current_max = tree_map[row, 0]
        for c in range(1, max_column):
            current = tree_map[row, c]
            if current > current_max:
                result.add((row, c))
                current_max = current

        current_max = tree_map[row, max_row]
        for c in range(max_column - 1, 0, -1):
            current = tree_map[row, c]
            if current > current_max:
                result.add((row, c))
                current_max = current

    for column in range(1, max_column):
        current_max = tree_map[0, column]
        for r in range(1, max_row):
            current = tree_map[r, column]
            if current > current_max:
                result.add((r, column))
                current_max = current

        current_max = tree_map[max_row, column]
        for r in range(max_row - 1, 0, -1):
            current = tree_map[r, column]
            if current > current_max:
                result.add((r, column))
                current_max = current

    return len(result) + 2 * max_row + 2 * max_column


example_input = '''30373
25512
65332
33549
35390'''.splitlines()

assert solution_for_first_part(example_input) == 21

# The input is taken from: https://adventofcode.com/2022/day/8/input
task_input = list(load_input_file('input.08.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterator[str]) -> int:
    max_row, max_column, tree_map = build_tree_map(task_input)

    def count_visible_trees(current, start, stop, step, take):
        trees = 1
        for coordinate in range(start, stop, step):
            if take(coordinate) >= current:
                break

            trees += 1

        return trees

    result = {}
    for row in range(1, max_row):
        for column in range(1, max_column):
            current_point = tree_map[row, column]

            visible_trees_up = count_visible_trees(current_point, column - 1, 0, -1, lambda c: tree_map[row, c])
            visible_trees_down = count_visible_trees(current_point, column + 1, max_column, 1, lambda c: tree_map[row, c])
            visible_trees_left = count_visible_trees(current_point, row - 1, 0, -1, lambda r: tree_map[r, column])
            visible_trees_right = count_visible_trees(current_point, row + 1, max_row, 1, lambda r: tree_map[r, column])

            result[row, column] = visible_trees_up * visible_trees_down * visible_trees_left * visible_trees_right

    return max(result.values())


print("Solution for the second part:", solution_for_second_part(task_input))
