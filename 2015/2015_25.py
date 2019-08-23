import re
import itertools


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read()    


def read_coordinates(input_file_content: str) -> (int, int):
    pattern = re.compile(r'To continue, please consult the code grid in the manual\.  Enter the code at row (\d+), column (\d+)\.')
    groups = pattern.match(input_file_content)
    return int(groups[1]), int(groups[2])


def sum_all_number_before(n):
    return (n * n + n) // 2


def coordinates_to_ordinal_number(row: int, column: int) -> int:
    return 1 + sum_all_number_before(row + column - 1) - row


def get_code_for_ordinal_number(ordinal_number: int) -> int:

    def code_generator():
        prev = 20151125
        while True:
            yield prev
            prev = (prev * 252533) % 33554393

    generator = code_generator()
    for _ in range(ordinal_number - 1):
        next(generator)

    return next(generator)


def solution_for_first_part(input: str) -> int:
    row, column = read_coordinates(input)
    ordinal_number = coordinates_to_ordinal_number(row, column)

    return get_code_for_ordinal_number(ordinal_number)


assert coordinates_to_ordinal_number(1, 1) == 1
assert coordinates_to_ordinal_number(1, 2) == 3
assert coordinates_to_ordinal_number(1, 6) == 21
assert coordinates_to_ordinal_number(2, 3) == 9
assert coordinates_to_ordinal_number(3, 3) == 13
assert coordinates_to_ordinal_number(4, 2) == 12
assert coordinates_to_ordinal_number(5, 2) == 17
assert coordinates_to_ordinal_number(6, 1) == 16

assert get_code_for_ordinal_number(1) == 20151125
assert get_code_for_ordinal_number(5) == 21629792
assert get_code_for_ordinal_number(10) == 30943339

# The input is taken from: https://adventofcode.com/2015/day/25/input
print("Solution for the first part:", solution_for_first_part(load_input_file('input.25.txt')))
