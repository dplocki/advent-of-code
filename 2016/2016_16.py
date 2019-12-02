def load_input_file(file_name: str):
    with open(file_name) as file:
        return file.read()


def code(a: str) -> str:
    return a + '0' + a[::-1].replace('0', ' ').replace('1', '0').replace(' ', '1')


def fill_the_disc(a, size):
    while len(a) <= size:
        a = code(a)

    return a[:size]


def calculate_checksum(a):

    def check_pairs(a):
        return ''.join(map(lambda x: '1' if x[0] == x[1] else '0', [a[i:i+2] for i in range(0, len(a), 2)]))

    result = check_pairs(a)
    while len(result) % 2 == 0:
        result = check_pairs(result)

    return result


def solution_for_first_part(input):
    disc_content = fill_the_disc(input, 272)
    return calculate_checksum(disc_content)


assert code('11111') == '11111000000'
assert code('111100001010') == '1111000010100101011110000'
assert fill_the_disc('10000', 20) == '10000011110010000111'
assert calculate_checksum('10000011110010000111') == '01100'

# The input is taken from: https://adventofcode.com/2016/day/16/input
input = load_input_file('input.16.txt')
print("Solution for the first part:", solution_for_first_part(input))


def solution_for_second_part(input):
    disc_content = fill_the_disc(input, 35651584)
    return calculate_checksum(disc_content)


print("Solution for the second part:", solution_for_second_part(input))
