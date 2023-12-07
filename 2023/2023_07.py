from typing import Generator, Iterable, Tuple
from itertools import count
import collections


FIVE_OF_KIND = 7
FOUR_OF_KIND = 6
FULL_HOUSE = 5
THREE_OF_KIND = 4
TWO_PAIRS = 3
ONE_PAIR = 2
HIGH_CARD = 1
CARD_VALUES = { card: card_value for card, card_value in zip('AKQJT98765432'[::-1], count(1))}


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[str, int], None, None]:
    for line in task_input:
        tokens = line.split()
        yield tokens[0], int(tokens[1])


def get_value_card(hand):
    individual_cards = collections.Counter(hand)
    individual_cards_count = len(individual_cards)

    if individual_cards_count == 1:
        return FIVE_OF_KIND

    counts = individual_cards.values()
    if individual_cards_count == 2:
        if 3 in counts:
            return FULL_HOUSE

        if 4 in counts:
            return FOUR_OF_KIND

    if individual_cards_count == 3:
        if 3 in counts:
            return THREE_OF_KIND

        if 2 in counts:
            return TWO_PAIRS

    if individual_cards_count == 4:
        return ONE_PAIR

    return HIGH_CARD


def hand_to_values(hand: str):
    return tuple(CARD_VALUES[card] for card in hand)


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return sum(
        index * bid
        for (_, bid), index in zip(sorted(parse(task_input), key=lambda pair: (get_value_card(pair[0]), *hand_to_values(pair[0]))), count(1)))


example_input = '''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483'''.splitlines()

assert solution_for_first_part(example_input) == 6440

# The input is taken from: https://adventofcode.com/2023/day/7/input
task_input = list(load_input_file('input.07.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
