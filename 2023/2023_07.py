from typing import Callable, Dict, Generator, Iterable, Tuple
from itertools import count
import collections


FIVE_OF_KIND = 7
FOUR_OF_KIND = 6
FULL_HOUSE = 5
THREE_OF_KIND = 4
TWO_PAIRS = 3
ONE_PAIR = 2
HIGH_CARD = 1


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[str, int], None, None]:
    for line in task_input:
        tokens = line.split()
        yield tokens[0], int(tokens[1])


def get_value_card(hand: str) -> int:
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


def get_hand_to_values_function(card_values: Dict[str, int]) -> Callable[[str], Tuple[int, int, int, int, int]]:

    def internal(hand: str) -> Tuple[int, int, int, int, int]:
        return tuple(card_values[card] for card in hand)


    return internal


def solution(task_input: Iterable[str], cards_sorted: str, get_value_card: Callable[[str], int]) -> int:
    hand_to_values = get_hand_to_values_function({ card: card_value for card, card_value in zip(cards_sorted[::-1], count(1))})

    return sum(
        index * bid
        for (_, bid), index in zip(sorted(parse(task_input), key=lambda pair: (get_value_card(pair[0]), *hand_to_values(pair[0]))), count(1)))


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return solution(task_input, 'AKQJT98765432', get_value_card)


example_input = '''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483'''.splitlines()

assert solution_for_first_part(example_input) == 6440

# The input is taken from: https://adventofcode.com/2023/day/7/input
task_input = list(load_input_file('input.07.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def get_hand_combinations(possibilities: Iterable[str], hand: str, index: int, prefix: str) -> Generator[str, None, None]:
    if index == 5:
        yield prefix
        return

    if hand[index] == 'J':
        for possibility in possibilities:
            yield from get_hand_combinations(possibilities, hand, index + 1, prefix + possibility)
    else:
        yield from get_hand_combinations(possibilities, hand, index + 1, prefix + hand[index])


def get_value_card_with_jokers(hand: str) -> int:
    if 'J' not in hand:
        return get_value_card(hand)

    if hand == 'JJJJJ':
        return FIVE_OF_KIND

    return max(get_value_card(h) for h in get_hand_combinations(set(card for card in hand if card != 'J'), hand, 0, ''))


def solution_for_second_part(task_input: Iterable[str]) -> int:
    return solution(task_input, 'AKQT98765432J', get_value_card_with_jokers)


assert solution_for_second_part(example_input) == 5905
print("Solution for the second part:", solution_for_second_part(task_input))