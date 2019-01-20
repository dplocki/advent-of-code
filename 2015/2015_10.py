def load_input_file(file_name):
    with open(file_name) as file:
        return file.read().strip()


def look_and_say(word: str):
    previous_letter = word[0]
    count_letters = 0

    for letter in word:
        if previous_letter == letter:
            count_letters += 1
        else:
            yield str(count_letters) + previous_letter

            count_letters = 1
            previous_letter = letter

    yield str(count_letters) + previous_letter


def generator_to_str(generator): return ''.join(generator)


def solution_for_first_part(initial_word: str):
    word = initial_word
    for _ in range(40):
        word = generator_to_str(look_and_say(word))

    return len(word)


assert generator_to_str(look_and_say('1')) == '11'
assert generator_to_str(look_and_say('11')) == '21'
assert generator_to_str(look_and_say('21')) == '1211'
assert generator_to_str(look_and_say('1211')) == '111221'
assert generator_to_str(look_and_say('111221')) == '312211'

# The solution is taken from: https://adventofcode.com/2015/day/10/input
print("Solution for the first part:", solution_for_first_part(load_input_file('input.10.txt')))
