def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def find_buttons(input: [str]):
    letter_to_vector_matrix = { 'U': 0, 'L': 1, 'R': 2, 'D': 3 }
    movie_matrix = {
        # U L R D
        1: [1, 1, 2, 4],
        2: [2, 1, 3, 5],
        3: [3, 2, 3, 6],
        4: [1, 4, 5, 7],
        5: [2, 4, 6, 8],
        6: [3, 5, 6, 9],
        7: [4, 7, 8, 7],
        8: [5, 7, 9, 8],
        9: [6, 8, 9, 9]
    }

    button = 5
    for line in input:
        for character in line:
            button = movie_matrix[button][letter_to_vector_matrix[character]]

        yield button


def solution_for_first_part(input):
    return ''.join(map(lambda x: str(x), find_buttons(input)))


test_input = '''ULL
RRDDD
LURDL
UUUUD'''.splitlines()


assert solution_for_first_part(test_input) == '1985'


# The input is taken from: https://adventofcode.com/2016/day/2/input
input = load_input_file('input.02.txt')
print("Solution for the first part:", solution_for_first_part(input))
