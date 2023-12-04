from typing import Generator, Iterable, Set, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[Set[int], Set[int]], None, None]:
    for line in task_input:
        numbers = line.split(':')[1]
        yield tuple(map(lambda token: set(map(int, token.strip().split())), numbers.split('|')))


def solution_for_first_part(task_input: Iterable[str]) -> int:
    result = 0
    for winning, numbers in parse(task_input):
        matched_numbers_count = len(winning.intersection(numbers))
        if matched_numbers_count > 0:
            result += 2 ** (matched_numbers_count - 1)

    return result


example_input = '''Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'''.splitlines()

assert solution_for_first_part(example_input) == 13

# The input is taken from: https://adventofcode.com/2023/day/4/input
task_input = list(load_input_file('input.04.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> int:
    cards = {index + 1: card for index, card in enumerate(parse(task_input)) }
    cards_number = { card: 1 for card in cards.keys() }

    for current_card_index, (winning, numbers) in cards.items():
        matched_numbers_count = len(winning.intersection(numbers))

        for next_card in range(current_card_index + 1, current_card_index + 1 + matched_numbers_count):
            cards_number[next_card] += cards_number.get(current_card_index, 0)

    return sum(cards_number.values())


print("Solution for the second part:", solution_for_second_part(task_input))