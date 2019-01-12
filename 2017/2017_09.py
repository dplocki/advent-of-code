import re

def first_part(input_content):

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


    if input == None:
        test(1, '{}')
        test(6, '{{{}}}')
        test(5, '{{},{}}')
        test(16, '{{{},{},{{}}}}')
        test(1, '{<a>,<a>,<a>,<a>}')
        test(9, '{{<a>},{<a>},{<a>},{<a>}}')
        test(9, '{{<!!>},{<!!>},{<!!>},{<!!>}}')
        test(3, '{{<a!>},{<a!>},{<a!>},{<ab>}}')
    else:
        result = calculate(input_content)
        print(f'Solution: {result}')


def second_part(input_content):
    result = 0
    input = re.sub(r'!.', '', input_content)
    for m in re.finditer(r'<.*?>', input):
        result += len(m.group(0)) - 2

    print(f"Solution: {result}")

# Taken from https://adventofcode.com/2017/day/9/input
with open('input.txt', 'r') as content_file:
    content = content_file.read()
    first_part(content)
    second_part(content)
