def load_input_file(file_name):
    with open(file_name) as file:
        return file.read().strip()


def solve_captcha(input, step):
    result = 0
    length = len(input)

    for index, digit in enumerate(input):
        prev = input[(index + step) % length]

        if digit == prev:
            result += int(digit)

    return result


def solution_for_first_path(input):
    return solve_captcha(input, 1)


def test_sample(input, expected, function):
    result = function(input)
    assert result == expected, f'{input}: Expected: {expected}: Gain: {result}'


def test_sample_a(input, expected):
    test_sample(input, expected, solution_for_first_path)


test_sample_a('1234', 0)
test_sample_a('1122', 3)
test_sample_a('1111', 4)
test_sample_a('91212129', 9)

# The input is taken from: https://adventofcode.com/2017/day/1/input
captcha = load_input_file('input.01.txt')
print("Solution for the first part:", solution_for_first_path(captcha))


def solution_for_second_path(input):
    return solve_captcha(input, int(len(input)/2))


def test_sample_b(input, expected):
    test_sample(input, expected, solution_for_second_path)


test_sample_b('1212', 6)
test_sample_b('1221', 0)
test_sample_b('123425', 4)
test_sample_b('123123', 12)
test_sample_b('12131415', 4)

print("Solution for the second part:", solution_for_second_path(captcha))
