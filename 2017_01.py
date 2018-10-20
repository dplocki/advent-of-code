def solve_captcha(input, step):
    result = 0
    lenght = len(input)

    for index, digit in enumerate(input):
        prev = input[(index + step) % lenght]

        if digit == prev:
            result += int(digit)

    return result


def solve_captcha_a(input):
    return solve_captcha(input, 1)


def solve_captcha_b(input):
    return solve_captcha(input, int(len(input)/2))


def test_sample(input, expected, function):
    result = function(input)
    assert result == expected, f'{input}: Expected: {expected}: Gain: {result}'


def test_sample_a(input, expected):
    test_sample(input, expected, solve_captcha_a)


def test_sample_b(input, expected):
    test_sample(input, expected, solve_captcha_b)


# Tests A
test_sample_a('1234', 0)
test_sample_a('1122', 3)
test_sample_a('1111', 4)
test_sample_a('91212129', 9)

# Tests B
test_sample_b('1212', 6)
test_sample_b('1221', 0)
test_sample_b('123425', 4)
test_sample_b('123123', 12)
test_sample_b('12131415', 4)

# Resolution
# Download the https://adventofcode.com/2017/day/1/input
# print(solve_captch_a(<put here>))
# print(solve_captch_b(<put here>))
