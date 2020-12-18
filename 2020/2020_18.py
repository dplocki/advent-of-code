def load_input_file(file_name: str) -> [str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse_line(line: str) -> list:
    return [c if c in '()+*' else int(c) for c in line.replace('(', '( ').replace(')',  ' )').split(' ')]


def parse(task_input: [str]):
    yield from (parse_line(line) for line in task_input)


def calculate(tokens: []) -> int:

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
            return calculate(tokens[:-2]) * tokens[-1]
        elif tokens[-2] == '+':
            return calculate(tokens[:-2]) + tokens[-1]
        else:
            raise Exception(f'Invalid token as operator: {tokens[-2]}')
    else:
        match_index = find_matching_bracket(tokens)

        return calculate(tokens[:match_index] + [calculate(tokens[match_index + 1:-1])])


def solution_for_first_part(task_input: [str]) -> int:
    return sum(calculate(line) for line in parse(task_input))


assert calculate(parse_line('1 + 2 * 3 + 4 * 5 + 6')) == 71
assert calculate(parse_line('1 + (2 * 3) + (4 * (5 + 6))')) == 51
assert calculate(parse_line('2 * 3 + (4 * 5)')) == 26
assert calculate(parse_line('5 + (8 * 3 + 9 + 3 * 4 * 3)')) == 437
assert calculate(parse_line('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))')) == 12240
assert calculate(parse_line('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2')) == 13632


# The input is taken from: https://adventofcode.com/2020/day/18/input
task_input = list(load_input_file('input.18.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
