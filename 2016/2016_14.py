import hashlib
import re


def load_input_file(file_name):
    with open(file_name) as file:
        return file.read()


def get_md5(already_known, password):
    if password in already_known:
        return already_known[password]

    md5 = hashlib.md5(password.encode('utf-8')).hexdigest()
    already_known[password] = md5

    return md5


def return_repeating_letters(source, how_many = 3):
    number = 0
    previous = None
    for letter in source:
        number = (number + 1) if letter == previous else 1
        if number == how_many:
            return letter

        previous = letter

    return None


def is_in_1000_four_letters(already_known, salt, letter, start_index):
    for index in range(start_index, start_index + 1000):
        md5 = get_md5(already_known, salt + str(index))
        if letter * 5 in md5:
            return True

    return False


def hashes_index_generator(salt):
    already_known = {}
    index = 1
    while True:
        md5 = get_md5(already_known, salt + str(index))
        letter = return_repeating_letters(md5)

        if letter != None and is_in_1000_four_letters(already_known, salt, letter, index + 1):
            yield index            

        index += 1


def solution_for_first_part(salt):
    for index, _ in zip(hashes_index_generator(salt), range(64)):
        pass

    return index


assert return_repeating_letters('xcmcvmncvaaaasd') == 'a'
assert return_repeating_letters('xcmcvmncvaasd') == None
assert return_repeating_letters('sssxcmcvmncvaasd') == 's'
assert solution_for_first_part('abc') == 22728

# The input is taken from: https://adventofcode.com/2016/day/14/input
salt = load_input_file('input.14.txt')
print("Solution for the first part:", solution_for_first_part(salt))
