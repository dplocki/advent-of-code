from collections import deque
from operator import mul


PLAYER_1_DECK = 0
PLAYER_2_DECK = 1


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def parse(task_input: [str]):

    def parse_deck(raw_deck: str) -> [int]:
        return map(int, raw_deck.splitlines()[1:])


    raw_decks = task_input.split('\n\n')
    return parse_deck(raw_decks[PLAYER_1_DECK]), parse_deck(raw_decks[PLAYER_2_DECK])


def solution_for_first_part(task_input):
    player1_deck, player2_deck = parse(task_input)
    player1_deck = deque(player1_deck)
    player2_deck = deque(player2_deck)

    while player1_deck and player2_deck:
        p1 = player1_deck.popleft()
        p2 = player2_deck.popleft()

        if p1 > p2:
            player1_deck.append(p1)
            player1_deck.append(p2)
        else:
            player2_deck.append(p2)
            player2_deck.append(p1)

    winer = player1_deck if player1_deck else player2_deck
    return sum(value * score for value, score in zip(winer, range(len(winer), 0, -1)))


example_input = '''Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10'''

assert solution_for_first_part(example_input) == 306

# The input is taken from: https://adventofcode.com/2020/day/22/input
task_input = load_input_file('input.22.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
