def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def find_buttons(input: [str], movie_matrix: {str: [str]}):
    letter_to_vector_matrix = { 'U': 0, 'L': 1, 'R': 2, 'D': 3 }
    button = '5'
    for line in input:
        for character in line:
            button = movie_matrix[button][letter_to_vector_matrix[character]]

        yield button


def buttons_list_to_single_line(input: [str]) -> str:
    return ''.join(input)


def solution_for_first_part(input):
    movie_matrix = {
        # U L R D
        '1': ['1', '1', '2', '4'],
        '2': ['2', '1', '3', '5'],
        '3': ['3', '2', '3', '6'],
        '4': ['1', '4', '5', '7'],
        '5': ['2', '4', '6', '8'],
        '6': ['3', '5', '6', '9'],
        '7': ['4', '7', '8', '7'],
        '8': ['5', '7', '9', '8'],
        '9': ['6', '8', '9', '9']
    }

    buttons = find_buttons(input, movie_matrix)

    return buttons_list_to_single_line(buttons)


def solution_for_second_part(input):
    movie_matrix = {
        # U L R D
        '1': ['1', '1', '1', '3'],
        '2': ['2', '1', '3', '6'],
        '3': ['1', '2', '4', '7'],
        '4': ['4', '3', '4', '8'],
        '5': ['5', '5', '6', '5'],
        '6': ['2', '5', '7', 'A'],
        '7': ['3', '6', '8', 'B'],
        '8': ['4', '7', '9', 'C'],
        '9': ['9', '8', '9', '9'],
        'A': ['6', 'A', 'B', 'A'],
        'B': ['7', 'A', 'C', 'D'],
        'C': ['8', 'B', 'C', 'C'],
        'D': ['B', 'D', 'D', 'D']
    }

    buttons = find_buttons(input, movie_matrix)

    return buttons_list_to_single_line(buttons)


test_input = '''ULL
RRDDD
LURDL
UUUUD'''.splitlines()


assert solution_for_first_part(test_input) == '1985'
assert solution_for_second_part(test_input) == '5DB3'

# The input is taken from: https://adventofcode.com/2016/day/2/input
input = list(load_input_file('input.02.txt'))
print("Solution for the first part:", solution_for_first_part(input))
print("Solution for the second part:", solution_for_second_part(input))
