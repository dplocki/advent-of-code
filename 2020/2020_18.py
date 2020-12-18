def load_input_file(file_name: str) -> [str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse_line(line: str) -> list:
    return [c if c in '()+*' else int(c) for c in line.replace('(', '( ').replace(')',  ' )').split(' ')]


def parse(task_input: [str]):
    yield from (parse_line(line) for line in task_input)


def calculate_first_part(tokens: []) -> int:

    def find_matching_bracket(tokens: list) -> int:
        match_count = 0
        for i, c in enumerate(tokens[::-1]):
            if c == ')': match_count += 1
            elif c == '(': match_count -= 1
            if match_count == 0:
                return len(tokens) - i - 1


    if len(tokens) == 0:
        return 0

    if len(tokens) == 1:
        return tokens[0]

    if tokens[-1] != ')':
        if tokens[-2] == '*':
            return calculate_first_part(tokens[:-2]) * tokens[-1]
        elif tokens[-2] == '+':
            return calculate_first_part(tokens[:-2]) + tokens[-1]
        else:
            raise Exception(f'Invalid token as operator: {tokens[-2]}')

    match_index = find_matching_bracket(tokens)
    return calculate_first_part(tokens[:match_index] + [calculate_first_part(tokens[match_index + 1:-1])])


def solution(task_input: [str], calculate) -> int:
    return sum(calculate(line) for line in parse(task_input))


assert calculate_first_part(parse_line('1 + 2 * 3 + 4 * 5 + 6')) == 71
assert calculate_first_part(parse_line('1 + (2 * 3) + (4 * (5 + 6))')) == 51
assert calculate_first_part(parse_line('2 * 3 + (4 * 5)')) == 26
assert calculate_first_part(parse_line('5 + (8 * 3 + 9 + 3 * 4 * 3)')) == 437
assert calculate_first_part(parse_line('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))')) == 12240
assert calculate_first_part(parse_line('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2')) == 13632


# The input is taken from: https://adventofcode.com/2020/day/18/input
task_input = list(load_input_file('input.18.txt'))
print("Solution for the first part:", solution(task_input, calculate_first_part))


def calculate_second_part(tokens: []):

    def find_matching_bracket(tokens):
        match_count = 1
        for i, c in enumerate(tokens):
            if c == '(': match_count +=1
            if c == ')':
                match_count -= 1
                if match_count == 0:
                    return i


    if len(tokens) == 0:
        return 0

    if len(tokens) == 1:
        return tokens[0]

    if '(' in tokens:
        bracket_index = tokens.index('(')
        index_of_matching_bracket = find_matching_bracket(tokens[bracket_index + 1:])
        return calculate_second_part(tokens[:bracket_index] + \
                [calculate_second_part(tokens[bracket_index + 1:bracket_index + index_of_matching_bracket + 1])] + \
                tokens[bracket_index + index_of_matching_bracket + 2:])

    if '+' in tokens:
        plus_index = tokens.index('+')
        return calculate_second_part(tokens[:plus_index - 1] + [tokens[plus_index - 1] + tokens[plus_index + 1]] + tokens[plus_index + 2:])

    if '*' in tokens:
        multiple_index = tokens.index('*')
        return calculate_second_part(tokens[:multiple_index - 1] + \
                [tokens[multiple_index - 1] * tokens[multiple_index + 1]] +\
                tokens[multiple_index + 2:])

    raise Exception('Incorrect expression')


assert calculate_second_part(parse_line('1 + (2 * 3) + (4 * (5 + 6))')) == 51
assert calculate_second_part(parse_line('2 * 3 + (4 * 5)')) == 46
assert calculate_second_part(parse_line('5 + (8 * 3 + 9 + 3 * 4 * 3)')) == 1445
assert calculate_second_part(parse_line('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))')) == 669060
assert calculate_second_part(parse_line('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2')) == 23340

print("Solution for the second part:", solution(task_input, calculate_second_part))
