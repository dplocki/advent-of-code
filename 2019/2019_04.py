def load_input_file(file_name: str):
    with open(file_name) as file:
        return map(int, file.read().strip().split('-'))


def pair_previous_with_current(sample):
    previous = ''

    for current in str(sample):
        yield previous, current
        previous = current


def check(sample):
    is_pair = False

    for p, c in pair_previous_with_current(sample):
        if p > c:
            return False

        if p == c:
            is_pair = True

    return is_pair


def solution_for_first_part(start_range, end_range):
    return sum([1 for sample in range(start_range, end_range + 1) if check(sample)])


assert check(112233) == True
assert check(223450) == False
assert check(123789) == False

# The input is taken from: https://adventofcode.com/2019/day/4/input
start_range, end_range = load_input_file('input.04.txt')
print("Solution for the first part:", solution_for_first_part(start_range, end_range))
