def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def swap_positions(password, a, b):
    password[a], password[b] = password[b], password[a]
    return password


def swap_letters(password: [str], a, b):
    return swap_positions(password, password.index(a), password.index(b))


def rotate_left(password, a, _):
    return password[a:] + password[:a]


def rotate_right(password, a, _):
    a = a % len(password)
    return password[-a:] + password[:len(password) - a] if a != 0 else password


def rotate_based(password, a, _):
    index_of_a = password.index(a)

    return rotate_right(password, index_of_a + 1 + (1 if index_of_a >= 4 else 0), _)


def reverse(password, a, b):
    return password[:a] + list(reversed(password[a:b + 1])) + password[b + 1:]


def move(password, a, b):
    letter = password[a]
    tmp = password[:a] + password[a + 1:]
    return tmp[:b] + [letter] + tmp[b:]


def parse(instruction_list: [str]):
    for instruction in instruction_list:
        tokens = instruction.split(' ')

        if instruction.startswith('swap position'):
            yield swap_positions, int(tokens[2]), int(tokens[5])
        elif instruction.startswith('swap letter'):
            yield swap_letters, tokens[2], tokens[5]
        elif instruction.startswith('rotate left'):
            yield rotate_left, int(tokens[2]), None
        elif instruction.startswith('rotate right'):
            yield rotate_right, int(tokens[2]), None
        elif instruction.startswith('rotate based'):
            yield rotate_based, tokens[6], None
        elif instruction.startswith('reverse'):
            yield reverse, int(tokens[2]), int(tokens[4])
        elif instruction.startswith('move position'):
            yield move, int(tokens[2]), int(tokens[5])


def run_parser(parser, instruction_list: [str], password):
    raw_password = list(password)
    for instruction, first_parameter, second_parameter in parser(instruction_list):
        raw_password = instruction(raw_password, first_parameter, second_parameter)

    return ''.join(raw_password)

def solution_for_first_part(instruction_list, password):
    return run_parser(parse, instruction_list, password)


assert swap_positions(list('abcde'), 4, 0) == list('ebcda')
assert swap_letters(list('ebcda'), 'd', 'b') == list('edcba')
assert reverse(list('edcba'), 0, 4) == list('abcde')
assert rotate_left(list('abcde'), 1, None) == list('bcdea')
assert move(list('bcdea'), 1, 4) == list('bdeac')
assert move(list('bdeac'), 3, 0) == list('abdec')
assert rotate_based(list('abdec'), 'b', None) == list('ecabd')
assert rotate_based(list('ecabd'), 'd', None) == list('decab')

test_input = '''swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d'''.splitlines()

assert solution_for_first_part(test_input, 'abcde') == 'decab'

# The input is taken from: https://adventofcode.com/2016/day/21/input
instructions = list(load_input_file('input.21.txt'))
print("Solution for the first part:", solution_for_first_part(instructions, 'abcdefgh'))


def solution_for_second_part(instruction_list: [str], password):

    def anty_rotate_based(value_table: {}):
        def anty_rotate_based_with_value_table(password, a, _):
            index_of_a = password.index(a)
            return rotate_left(password, value_table[index_of_a], _)

        return anty_rotate_based_with_value_table

    def reversing_parser(original_parser):

        def build_anty_rotate_based_to_left_table():
            base = list('abcdefgh')
            for letter in base:
                reversed_password = rotate_based(base[:], letter, None)
                yield reversed_password.index(letter), reversed_password.index('a')

        anty_rotate_based_to_left_table = {k: v for k, v in build_anty_rotate_based_to_left_table()}

        reversed_instruction_list = reversed(list(parse(instruction_list)))
        for instruction, first_parameter, second_parameter in reversed_instruction_list:
            if instruction in [swap_positions, swap_letters, move]:
                yield instruction, second_parameter, first_parameter
            elif instruction == rotate_left:
                yield rotate_right, first_parameter, second_parameter
            elif instruction == rotate_right:
                yield rotate_left, first_parameter, second_parameter
            elif instruction == rotate_based:
                yield anty_rotate_based(anty_rotate_based_to_left_table), first_parameter, second_parameter
            else:
                yield instruction, first_parameter, second_parameter


    return run_parser(reversing_parser, instruction_list, password)


def test_of_descrambling(instructions, password):
    reversed_password = solution_for_first_part(instructions, password)
    result = solution_for_second_part(instructions, reversed_password)
    assert result == password, f"Expected '{password}' recived: '{result}'"


for l in 'abcdefgh':
    test_of_descrambling([f'rotate based on position of letter {l}'], 'abcdefgh')


print("Solution for the second part:", solution_for_second_part(instructions, 'fbgdceah'))
