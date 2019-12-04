def load_input_file(file_name: str):
    with open(file_name) as file:
        return map(int, file.read().strip().split('-'))


def pair_previous_with_current(sample):
    previous = ''

    for current in str(sample):
        yield previous, current
        previous = current


def check_for_first_part(sample):
    is_pair = False

    for p, c in pair_previous_with_current(sample):
        if p > c:
            return False

        if p == c:
            is_pair = True

    return is_pair


def count_maching_password_in_range(start_range, end_range, check):
    return sum([1 for sample in range(start_range, end_range + 1) if check(sample)])


assert check_for_first_part(112233) == True
assert check_for_first_part(223450) == False
assert check_for_first_part(123789) == False

# The input is taken from: https://adventofcode.com/2019/day/4/input
start_range, end_range = load_input_file('input.04.txt')
print("Solution for the first part:", count_maching_password_in_range(start_range, end_range, check_for_first_part))


def check_for_second_part(sample):
    groups = '.'
    for p, c in pair_previous_with_current(sample):
        if p > c:
            return False

        groups += '^' if p == c else '.'

    groups += '.'
    return '.^.' in groups


assert check_for_second_part(112233) == True
assert check_for_second_part(123444) == False
assert check_for_second_part(111122) == True

print("Solution for the second part:", count_maching_password_in_range(start_range, end_range, check_for_second_part))
