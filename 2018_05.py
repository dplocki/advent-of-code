import string


def react_simpulator(input):
    letter_combinations = [letter + letter.upper() for letter in string.ascii_lowercase] + [letter.upper() + letter for letter in string.ascii_lowercase]

    previous_lenght = 0
    current_lenght = len(input)

    while previous_lenght != current_lenght: 
        previous_lenght = current_lenght

        for letter_combination in letter_combinations:
            input = input.replace(letter_combination, '')

        current_lenght = len(input)

    return current_lenght


assert react_simpulator('dabAcCaCBAcCcaDA') == 10

# See: https://adventofcode.com/2018/day/5/input
print("Solution for first part:", react_simpulator('<puzzle input>'))
