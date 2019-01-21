import itertools
import re


def load_input_file(file_name):
    with open(file_name) as file:
        return file.read().strip()


def generate_next_word(start: str):


    def increment(start: str):
        result = ''
        move = True

        for c in reversed(start):
            if not move:
                result += c
                continue

            if c == 'z':
                move = True
                result += 'a'
            else:
                result += chr(ord(c) + 1)
                move = False

        if move:
            result += 'a'

        return result[::-1]


    while True:
        start = increment(start)
        yield start



def solution_for_first_part(old_santa_password):


    DOUBLE_PAIR_PATTERN = re.compile(r'.*(.)\1.*(.)\2.*')


    def passwords_must_include_one_increasing_straight(password):
        _a, _b, _c = itertools.tee(password, 3)
        next(_b)
        next(_c)
        next(_c)

        for a, b, c in zip(_a, _b, _c):
            if ord(a) + 2 == ord(b) + 1 == ord(c):
                return True

        return False


    def passwords_may_not_contain_the_letters_i_o_or_l(password):
        return 'i' not in password and 'o' not in password and 'l' not in password


    def passwords_must_contain_at_least_two_different_non_overlapping_pairs(password):
        result = DOUBLE_PAIR_PATTERN.match(password)

        return result and result[1] != result[2]


    for new_password in generate_next_word(old_santa_password):
        if not passwords_may_not_contain_the_letters_i_o_or_l(new_password):
            continue

        if not passwords_must_include_one_increasing_straight(new_password):
            continue

        if not passwords_must_contain_at_least_two_different_non_overlapping_pairs(new_password):
            continue

        return new_password


# The solution is taken from: https://adventofcode.com/2015/day/11/input
old_santa_password = load_input_file('input.11.txt')
print("Solution for the first part:", solution_for_first_part(old_santa_password))
