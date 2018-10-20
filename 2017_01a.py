def solve_captcha(input):
    result = 0
    lenght = len(input)

    for index, digit in enumerate(input):
        prev = input[(index + 1) % lenght]

        if digit == prev:
            result += int(digit)

    return result


def test_sample(input, expected):
    result = solve_captcha(input)
    assert result == expected

# Tests
test_sample('1234', 0)
test_sample('1122', 3)
test_sample('1111', 4)
test_sample('91212129', 9)

# Resolution
# Download the https://adventofcode.com/2017/day/1/input
# print(solve_captcha(<put here>))
