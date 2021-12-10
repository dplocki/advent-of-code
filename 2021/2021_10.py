OPEN_TOKENS = '[({<'
CLOSE_TOKENS = '])}>'


def load_input_file(file_name: str) -> list[str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def find_opening(token):
    return OPEN_TOKENS[CLOSE_TOKENS.index(token)]


def solution_for_first_part(task_input):
    result = 0
    for line in task_input:
        open_chunks = []
        for character in line:
            if character in OPEN_TOKENS:
                open_chunks.append(character)
            elif character in CLOSE_TOKENS:
                open_chunk = open_chunks.pop()
                if find_opening(character) != open_chunk:
                    if character == ')':
                        result += 3
                    if character == ']':
                        result += 57
                    if character == '}':
                        result += 1197
                    if character == '>':
                        result += 25137

                    continue
            else:
                raise Exception('Unexcepted character')

    return result


example_input = '''[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]'''.splitlines()

assert solution_for_first_part(example_input) == 26397

# The input is taken from: https://adventofcode.com/2021/day/10/input
task_input = list(load_input_file('input.10.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
