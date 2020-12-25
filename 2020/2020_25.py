from itertools import count


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def parse(task_input):
    lines = task_input.splitlines()
    return int(lines[0]), int(lines[1])


def transforms_subject_number(number: int) -> int:
    result = 1
    while True:
        result *= number
        result %= 20201227
        yield result


def find_secret_loop(reqest):
    for i, result in enumerate(transforms_subject_number(7)):
        if reqest == result:
            return i + 1


def calculate_encryption_key(public_key, secret_card_loop):
    for result, _ in zip(transforms_subject_number(public_key), range(secret_card_loop)):
        pass

    return result


def solution_for_first_part(task_input):
    door_public_key, card_public_key = parse(task_input)
    secret_card_loop = find_secret_loop(card_public_key)

    return calculate_encryption_key(door_public_key, secret_card_loop)


example_input = '''5764801
17807724'''

assert solution_for_first_part(example_input) == 14897079

# The input is taken from: https://adventofcode.com/2020/day/25/input
task_input = load_input_file('input.25.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
