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


def solution_for_first_part(instruction_list: [str], password):
    raw_password = list(password)
    for instruction, first_parameter, second_parameter in parse(instruction_list):
        raw_password = instruction(raw_password, first_parameter, second_parameter)

    return ''.join(raw_password)


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
rotate based on position of letter d'''

assert solution_for_first_part(test_input.splitlines(), 'abcde') == 'decab'

# The input is taken from: https://adventofcode.com/2016/day/21/input
instructions = load_input_file('input.21.txt')
print("Solution for the first part:", solution_for_first_part(instructions, 'abcdefgh'))
