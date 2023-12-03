from typing import Generator, Iterable, Set, Tuple
from functools import reduce
from operator import mul


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


class NumericValue():
    def __init__(self, value: int, position: int) -> None:
        self.value = value
        self.position = position

    def __hash__(self) -> int:
        return self.position


def get_int_value(source: NumericValue) -> int:
    return source.value


def return_neighboring_values(numeric_values: Set[Tuple[int, int]], row_index: int, column_index: int) -> Generator[NumericValue, None, None]:
    for tr, tc in ((-1, -1), (0, -1), (1, -1), (-1, 0),  (1, 0), (-1, 1), (0, 1), (1, 1)):
        if (row_index + tr, column_index + tc) in numeric_values:
            yield numeric_values[row_index + tr, column_index + tc]


def read_map(task_input: Iterable[str]):
    numeric_values = {}
    symbols = {}

    found_number = True
    for row_index, row in enumerate(task_input):
        row += '.'
        found_number = False
        number_size = 0
        current_number = 0

        for column_index, current_character in enumerate(row):
            if current_character.isnumeric():
                if found_number:
                    current_number = current_number * 10 + int(current_character)
                    number_size += 1
                else:
                    current_number = int(current_character)
                    number_size = 1
                    found_number = True
            else:
                if found_number:
                    value = NumericValue(current_number, row_index * (len(row) - 1) + column_index - number_size - 1)

                    for index in range(column_index - number_size, column_index):
                        numeric_values[row_index, index] = value

                    found_number = False
                    number_size = 0
                else:
                    found_number = False
                    number_size = 0
                    current_number = 0

                if current_character != '.':
                    symbols[row_index, column_index] = current_character

    return numeric_values, symbols


def solution_for_first_part(task_input: Iterable[str]) -> int:
    numeric_values, symbols = read_map(task_input)
    adjustment_numbers = set()

    for row_index, column_index in symbols.keys():
        adjustment_numbers.update(return_neighboring_values(numeric_values, row_index, column_index))

    return sum(map(get_int_value, adjustment_numbers))


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


def solution_for_second_part(task_input: Iterable[str]) -> int:
    numeric_values, symbols = read_map(task_input)
    adjustment_numbers = set()
    gears = (location for location, value in symbols.items() if value == '*')
    result = 0

    for row_index, column_index in gears:
        adjustment_numbers = set(return_neighboring_values(numeric_values, row_index, column_index))
        if len(adjustment_numbers) == 2:
            result += reduce(mul, map(get_int_value, adjustment_numbers))

    return result


assert solution_for_second_part(example_input) == 467835
print("Solution for the second part:", solution_for_second_part(task_input))
