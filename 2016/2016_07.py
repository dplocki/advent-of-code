import re


def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def split_line(line: str):
    yield from re.split(r'\[|\]', line)


def take_4_characters_sets(line: str):
    for index in range(len(line) - 3):
        yield line[index:index+4]


def check_for_abba(line: str) -> bool:
    for substring in take_4_characters_sets(line):
        if substring[0] != substring[1] and substring[0] == substring[3] and substring[1] == substring[2]:
            return True

    return False


def check_tls_supports(line: str) -> True:
    has_abba_outside = False
    for substring, outside in map(lambda x: (x[1], x[0] % 2 == 1), enumerate(split_line(line))):
        if outside and check_for_abba(substring):
            return False

        if not has_abba_outside:
            has_abba_outside = check_for_abba(substring)

    return has_abba_outside


assert check_tls_supports('abba[mnop]qrst') == True
assert check_tls_supports('abcd[bddb]xyyx') == False
assert check_tls_supports('aaaa[qwer]tyui') == False
assert check_tls_supports('ioxxoj[asdfgh]zxcvbn') == True


def solution_for_first_part(input_lines: [str]):
    return sum(1 for line in input_lines if check_tls_supports(line))


# The input is taken from: https://adventofcode.com/2016/day/7/input
input = load_input_file('input.07.txt')
print("Solution for the first part:", solution_for_first_part(input))
