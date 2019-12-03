def load_input_file(file_name: str):
    with open(file_name) as file:
        return [letter == '.' for letter in file.read() if letter in '.^']


def next_row(prev_row):

    def build_row(prev_row):
        length = len(prev_row)
        for i in range(length):
            left = bool(i == 0) or prev_row[i - 1]
            right = bool(i + 1 >= length) or prev_row[i + 1]

            yield left == right


    return list(build_row(prev_row))


def generate_rows(row, how_much):
    for _ in range(how_much):
        yield row
        row = next_row(row)


def count_safe_tiles(first_row, how_much):
    return sum([
            row.count(True)
            for row in generate_rows(first_row, how_much)
        ])


# The input is taken from: https://adventofcode.com/2016/day/18/input
first_row = load_input_file('input.18.txt')
print("Solution for the first part:", count_safe_tiles(first_row, 40))
print("Solution for the second part:", count_safe_tiles(first_row, 400_000))
