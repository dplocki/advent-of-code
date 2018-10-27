import re


def clean_up(input: str):
    return re.sub(r'<.*?>', '', re.sub(r'!.', '', input))


def calculate(input: str):
    input = clean_up(input)

    score = 0
    result = 0

    for char in input:
        if char == '{':
            score += 1
            result += score
        elif char == '}':
            score -= 1

    return result


def test(expected: int, input: str):
    result = calculate(input)
    assert result == expected, f"Expected: {expected} get: {result}"


test(1, '{}')
test(6, '{{{}}}')
test(5, '{{},{}}')
test(16, '{{{},{},{{}}}}')
test(1, '{<a>,<a>,<a>,<a>}')
test(9, '{{<a>},{<a>},{<a>},{<a>}}')
test(9, '{{<!!>},{<!!>},{<!!>},{<!!>}}')
test(3, '{{<a!>},{<a!>},{<a!>},{<ab>}}')


with open('input.txt', 'r') as content_file:
    content = content_file.read()
    result = calculate(content)

    print(f'Solution: {result}')
