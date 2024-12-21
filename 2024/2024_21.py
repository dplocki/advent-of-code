from typing import Dict, Generator, Iterable, Set, Tuple


def str_to_keypad(pattern: str) -> Dict[str, Tuple[int, int]]:
    return {
        letter: (row, column)
        for row, line in enumerate(pattern.splitlines())
        for column, letter in enumerate(line)
        if letter != ' '
    }


DIGITS_PAD = str_to_keypad('789\n456\n123\n 0A')
DIRECTIONAL_SECOND_PAD = str_to_keypad(' ^A\n<v>')


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def generate_sequences_from_letter_to_letter(key_pad: Dict[str, Tuple[int, int]], start: str, end: str) -> Generator[str, None, None]:
    to_check = [ (start, '') ]
    while to_check:
        current_position, path = to_check.pop()

        target = key_pad[end]
        if current_position == key_pad[end]:
            yield path
            continue

        column_move = target[1] - current_position[1]
        if column_move != 0:
            new_point = current_position[0], current_position[1] + (column_move // abs(column_move))
            if new_point in key_pad.values():
                if column_move > 0:
                    to_check.append((new_point, path +  '>'))
                elif column_move < 0:
                    to_check.append((new_point, path +  '<'))

        row_move = target[0] - current_position[0]
        if row_move != 0:
            new_point = current_position[0] + (row_move // abs(row_move)), current_position[1]
            if new_point in key_pad.values():
                if row_move > 0:
                    to_check.append((new_point, path +  'v'))
                elif row_move < 0:
                    to_check.append((new_point, path +  '^'))


def generate_sequences_for_code(key_pad: Dict[str, Tuple[int, int]], code: str) -> Set[str]:
    current_position = key_pad['A']
    solutions = set()
    solutions.add('')

    for letter in code:
        solutions = set(
            solution + sequence  + 'A'
            for sequence in generate_sequences_from_letter_to_letter(key_pad, current_position, letter)
            for solution in solutions)

        current_position = key_pad[letter]

    return solutions


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return sum(
            int(code[:-1]) * min(len(third_sequence)
                for first_sequence in generate_sequences_for_code(DIGITS_PAD, code)
                for second_sequence in generate_sequences_for_code(DIRECTIONAL_SECOND_PAD, first_sequence)
                for third_sequence in generate_sequences_for_code(DIRECTIONAL_SECOND_PAD, second_sequence))
            for code in task_input)


example_input = '''029A
980A
179A
456A
379A'''.splitlines()

assert solution_for_first_part(example_input) == 126384

# The input is taken from: https://adventofcode.com/2024/day/21/input
task_input = list(load_input_file('input.21.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
