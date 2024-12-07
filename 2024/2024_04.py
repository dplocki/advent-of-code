from typing import Generator, Iterable, List, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[int, int, str], None, None]:
    for row, line in enumerate(task_input):
        for column, character in enumerate(line):
            yield row, column, character


def find_word(letters_map, row, column) -> Generator[str, None, None]:
    yield letters_map.get((row, column), '') + letters_map.get((row + 1, column), '') + letters_map.get((row + 2, column), '') + letters_map.get((row + 3, column), '')
    yield letters_map.get((row, column), '') + letters_map.get((row - 1, column), '') + letters_map.get((row - 2, column), '') + letters_map.get((row - 3, column), '')
    yield letters_map.get((row, column), '') + letters_map.get((row, column + 1), '') + letters_map.get((row, column + 2), '') + letters_map.get((row, column + 3), '')
    yield letters_map.get((row, column), '') + letters_map.get((row, column - 1), '') + letters_map.get((row, column - 2), '') + letters_map.get((row, column - 3), '')
    yield letters_map.get((row, column), '') + letters_map.get((row + 1, column + 1), '') + letters_map.get((row + 2, column + 2), '') + letters_map.get((row + 3, column + 3), '')
    yield letters_map.get((row, column), '') + letters_map.get((row - 1, column - 1), '') + letters_map.get((row - 2, column - 2), '') + letters_map.get((row - 3, column - 3), '')
    yield letters_map.get((row, column), '') + letters_map.get((row + 1, column - 1), '') + letters_map.get((row + 2, column - 2), '') + letters_map.get((row + 3, column - 3), '')
    yield letters_map.get((row, column), '') + letters_map.get((row - 1, column + 1), '') + letters_map.get((row - 2, column + 2), '') + letters_map.get((row - 3, column + 3), '')


def solution_for_first_part(task_input: Iterable[str]) -> int:
    letters_map = {(row, column): character for row, column, character in parse(task_input)}

    max_rows = max(r for r, _ in letters_map.keys()) + 1
    max_columns = max(c for _, c in letters_map.keys()) + 1

    return sum(1
        for row in range(max_rows)
        for column in range(max_columns)
        for word in find_word(letters_map, row, column)
        if word == 'XMAS')


example_input = '''MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX'''.splitlines()

assert solution_for_first_part(example_input) == 18

# The input is taken from: https://adventofcode.com/2024/day/4/input
task_input = list(load_input_file('input.04.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
