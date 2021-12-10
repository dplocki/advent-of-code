from functools import reduce


OPEN_TOKENS = '[({<'
CLOSE_TOKENS = '])}>'


def load_input_file(file_name: str) -> list[str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def find_opening(token: str) -> str:
    return OPEN_TOKENS[CLOSE_TOKENS.index(token)]


def find_closing(token: str) -> str:
    return CLOSE_TOKENS[OPEN_TOKENS.index(token)]


def parser(lines: list[str]) -> list[tuple[int, str]]:

    def parse_line(line: str) -> tuple[int, str]:
        opening_chunks = []
        for character in line:
            if character in OPEN_TOKENS:
                opening_chunks.append(character)
            elif character in CLOSE_TOKENS:
                open_chunk = opening_chunks.pop()
                if find_opening(character) != open_chunk:
                    opening_chunks.append(character)
                    return True, opening_chunks

        return False, opening_chunks


    yield from (parse_line(line) for line in lines)


def solution_for_first_part(task_input: list[str]) -> int:
    score = { ')': 3, ']': 57, '}': 1197, '>': 25137 }
    return sum(score[stack.pop()] for is_corrupted, stack in parser(task_input) if is_corrupted)


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


def solution_for_second_part(task_input: list[str]) -> int:
    score = { ')': 1, ']': 2, '}': 3, '>': 4 }
    score_count = lambda result, current: result * 5 + score[find_closing(current)]

    stack_from_incomplete = [reversed(stack) for is_corrupted, stack in parser(task_input) if not is_corrupted]
    scores_per_lines = [reduce(score_count, stack, 0) for stack in stack_from_incomplete]

    return sorted(scores_per_lines)[len(scores_per_lines) // 2]


assert solution_for_second_part(example_input) == 288957
print("Solution for the second part:", solution_for_second_part(task_input))
