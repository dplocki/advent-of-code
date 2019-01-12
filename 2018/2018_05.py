import string


LETTER_COMBINATIONS = [letter + letter.upper() for letter in string.ascii_lowercase] + [letter.upper() + letter for letter in string.ascii_lowercase]


def calculate_length_after_all_reactions(input: str):
    previous_length = 0
    current_length = len(input)

    while previous_length != current_length: 
        previous_length = current_length

        for letter_combination in LETTER_COMBINATIONS:
            input = input.replace(letter_combination, '')

        current_length = len(input)

    return current_length


def find_the_shortes_polymer(input: str):
    return min([
        calculate_length_after_all_reactions(input.replace(letter, '').replace(letter.upper(), ''))
        for letter in string.ascii_lowercase
    ])


assert calculate_length_after_all_reactions('dabAcCaCBAcCcaDA') == 10

# See: https://adventofcode.com/2018/day/5/input
puzzle_input = '<puzzle input>'
print("Solution for first part:", calculate_length_after_all_reactions(puzzle_input))

assert find_the_shortes_polymer('dabAcCaCBAcCcaDA') == 4

print("Solution for second part:", find_the_shortes_polymer(puzzle_input))
