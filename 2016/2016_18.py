def load_input_file(file_name: str):
    with open(file_name) as file:
        return [letter == '.' for letter in file.read() if letter in '.^']


def next_row(prev_row):

    def build_row(prev_row):
        length = len(prev_row)
        for i in range(length):
            left = bool(i == 0) or prev_row[i - 1]
            center = prev_row[i]
            right = bool(i + 1 >= length) or prev_row[i + 1]

            yield not ((not left and not center and right) \
                or (not center and not right and left) \
                or (not left and center and right) \
                or (left and center and not right))


    return list(build_row(prev_row))


def solution_for_first_part(first_row):

    def generate_40_rows(row):
        for _ in range(40):
            yield row
            row = next_row(row)

    return sum([sum([1 for c in row if c]) for row in generate_40_rows(first_row)])


# The input is taken from: https://adventofcode.com/2016/day/18/input
first_row = load_input_file('input.18.txt')
print("Solution for the first part:", solution_for_first_part(first_row))
