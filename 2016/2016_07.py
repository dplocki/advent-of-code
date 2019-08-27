import re


def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def split_line(line: str):
    yield from re.split(r'\[|\]', line)


def take_characters_sets(line: str, characters_number):
    for index in range(len(line) - characters_number + 1):
        yield line[index:index+characters_number]


def check_for_abba(line: str) -> bool:
    for substring in take_characters_sets(line, 4):
        if substring[0] != substring[1] and substring[0] == substring[3] and substring[1] == substring[2]:
            return True

    return False


def check_tls_support(line: str) -> True:
    has_abba_outside = False
    for substring, outside in map(lambda x: (x[1], x[0] % 2 == 1), enumerate(split_line(line))):
        if outside and check_for_abba(substring):
            return False

        if not has_abba_outside:
            has_abba_outside = check_for_abba(substring)

    return has_abba_outside


assert check_tls_support('abba[mnop]qrst') == True
assert check_tls_support('abcd[bddb]xyyx') == False
assert check_tls_support('aaaa[qwer]tyui') == False
assert check_tls_support('ioxxoj[asdfgh]zxcvbn') == True


def count_the_supports(input_lines, is_support):
    return sum(1 for line in input_lines if is_support(line))


def solution_for_first_part(input_lines: [str]):
    return count_the_supports(input_lines, check_tls_support)


def find_aba(line: str):
    for substring in take_characters_sets(line, 3):
        if substring[0] != substring[1] and substring[0] == substring[2]:
            yield substring


def check_for_ssl_support(line: str):
    aba_outside, aba_inside = set(), set()

    for substring, outside in map(lambda x: (x[1], x[0] % 2 == 1), enumerate(split_line(line))):
        for aba in find_aba(substring):
            if outside:
                aba_outside.add((aba[1], aba[0]))
            else:
                aba_inside.add((aba[0], aba[1]))

    return len(aba_inside.intersection(aba_outside)) > 0


assert check_for_ssl_support('aba[bab]xyz') == True
assert check_for_ssl_support('xyx[xyx]xyx') == False
assert check_for_ssl_support('aaa[kek]eke') == True
assert check_for_ssl_support('zazbz[bzb]cdb') == True


def solution_for_second_part(input_lines: [str]):
    return count_the_supports(input_lines, check_for_ssl_support)


# The input is taken from: https://adventofcode.com/2016/day/7/input
input_lines = list(load_input_file('input.07.txt'))
print("Solution for the first part:", solution_for_first_part(input_lines))
print("Solution for the second part:", solution_for_second_part(input_lines))
