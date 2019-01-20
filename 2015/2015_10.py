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


def interation_generator(initial_word: str):
    word = initial_word
    i = 0
    while True:
        word = generator_to_str(look_and_say(word))
        i += 1
        yield i, word


def get_length_after_iteration(generator, require_iteration):
    for i, word in generator:
        if i < require_iteration:
            continue

        return len(word)


assert generator_to_str(look_and_say('1')) == '11'
assert generator_to_str(look_and_say('11')) == '21'
assert generator_to_str(look_and_say('21')) == '1211'
assert generator_to_str(look_and_say('1211')) == '111221'
assert generator_to_str(look_and_say('111221')) == '312211'

# The solution is taken from: https://adventofcode.com/2015/day/10/input
look_and_say_generator = interation_generator(load_input_file('input.10.txt'))

print("Solution for the first part:", get_length_after_iteration(look_and_say_generator, 40))
print("Solution for the second part:", get_length_after_iteration(look_and_say_generator, 50))
