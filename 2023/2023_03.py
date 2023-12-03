from typing import Dict, Generator, Iterable, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def check(whole_picture: Dict[Tuple[int, int], str], row_index: int, column_index: int, number_size: int) -> bool:
    for r in range(row_index - 1, row_index + 2):
        for c in range(column_index - 1 - number_size, column_index + 1):
            if whole_picture.get((r, c), '.') not in '.0123456789':
                return True

    return False


def solution_for_first_part(task_input: Iterable[str]) -> int:
    whole_picture = {}

    for row_index, row in enumerate(task_input):
        for column_index, column in enumerate(row):
            whole_picture[row_index, column_index] = column

    xs = [x for x, _ in whole_picture.keys()]
    ys = [y for _, y in whole_picture.keys()]
    max_x = max(xs)
    max_y = max(ys)

    result = 0
    for row_index in range(0, max_x + 1):
        found_number = False
        number_size = 0
        current_number = 0

        for column_index in range(0, max_y + 2):
            current_character = whole_picture.get((row_index, column_index), '.')

            if found_number:
                if current_character in '0123456789':
                    current_number = current_number * 10 + int(whole_picture[row_index, column_index])
                    number_size += 1
                else:
                    if check(whole_picture, row_index, column_index, number_size):
                        result += current_number

                    found_number = False
                    number_size = 0
            else:
                if current_character in '0123456789':
                    current_number = int(current_character)
                    number_size = 1
                    found_number = True
                else:
                    found_number = False
                    number_size = 0
                    current_number = 0


    return result


example_input = '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..'''.splitlines()

assert solution_for_first_part(example_input) == 4361

# The input is taken from: https://adventofcode.com/2023/day/3/input
task_input = list(load_input_file('input.03.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
