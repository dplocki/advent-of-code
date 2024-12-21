from functools import cache
from typing import Dict, Generator, Iterable, Set, Tuple


def sign(x: int) -> int:
    return 1 if x > 0 else -1 if x < 0 else 0


def str_to_keypad(pattern: str) -> Dict[str, Tuple[int, int]]:
    return {
        letter: (row, column)
        for row, line in enumerate(pattern.splitlines())
        for column, letter in enumerate(line)
        if letter != ' '
    }


DIGITS_PAD = 0
DIRECTIONAL_PAD = 1
KEYS_PAD = {
    DIGITS_PAD: str_to_keypad('789\n456\n123\n 0A'),
    DIRECTIONAL_PAD: str_to_keypad(' ^A\n<v>')
}


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def generate_sequences_from_letter_to_letter(key_pad: str, start: str, end: str) -> Generator[str, None, None]:
    to_check = [ (start, '') ]
    while to_check:
        current_position, path = to_check.pop()

        target = KEYS_PAD[key_pad][end]
        if current_position == target:
            yield path
            continue

        column_move = target[1] - current_position[1]
        if column_move != 0:
            new_point = current_position[0], current_position[1] + sign(column_move)
            if new_point in KEYS_PAD[key_pad].values():
                if column_move > 0:
                    to_check.append((new_point, path +  '>'))
                elif column_move < 0:
                    to_check.append((new_point, path +  '<'))

        row_move = target[0] - current_position[0]
        if row_move != 0:
            new_point = current_position[0] + sign(row_move), current_position[1]
            if new_point in KEYS_PAD[key_pad].values():
                if row_move > 0:
                    to_check.append((new_point, path +  'v'))
                elif row_move < 0:
                    to_check.append((new_point, path +  '^'))


@cache
def get_minimal_sequence_length(key_pad: str, code: str, robots_chain_size: int) -> int:
    if robots_chain_size == 0:
        return len(code)

    current_position = KEYS_PAD[key_pad]['A']
    minimal_length = 0

    for letter in code:
        minimal_length += min(
            get_minimal_sequence_length(DIRECTIONAL_PAD, sequence  + 'A', robots_chain_size - 1)
            for sequence in generate_sequences_from_letter_to_letter(key_pad, current_position, letter))

        current_position = KEYS_PAD[key_pad][letter]

    return minimal_length


def solution(task_input: Iterable[str], robot_chain_size: int) -> int:
    return sum(
        int(code[:-1]) * get_minimal_sequence_length(DIGITS_PAD, code, robot_chain_size + 1)
        for code in task_input)


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return solution(task_input, 2)


example_input = '''029A
980A
179A
456A
379A'''.splitlines()

assert solution_for_first_part(example_input) == 126384

# The input is taken from: https://adventofcode.com/2024/day/21/input
task_input = list(load_input_file('input.21.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> int:
    return solution(task_input, 25)


print("Solution for the second part:", solution_for_second_part(task_input))
