from collections import defaultdict
from itertools import product


CIRCLE_SIZE = 10


def load_input_file(file_name: str) -> list[str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: list[str]) -> tuple[int, int]:
    return tuple(int(line[-1]) for line in task_input)


def move_player(start: int, how_much: int) -> int:
    return ((start - 1 + how_much) % CIRCLE_SIZE) + 1


def solution_for_first_part(task_input: list[str]) -> int:

    def die_roll() -> list[tuple[int, int]]:
        use_count = 1
        while True:
            for value in range(100):
                yield value + 1, use_count
                use_count += 1


    player1, player2 = parse(task_input)

    die = die_roll()
    player1_score = 0
    player2_score = 0

    while True:
        for _ in range(3):
            value, count = next(die)
            player1 = move_player(player1, value)
        
        player1_score += player1

        if player1_score >= 1000:
            return player2_score * count
            
        for _ in range(3):
            value, count = next(die)
            player2 = move_player(player2, value)

        player2_score += player2
        
        if player2_score >= 1000:
            return player1_score * count


example_input = '''Player 1 starting position: 4
Player 2 starting position: 8'''.splitlines()

assert solution_for_first_part(example_input) == 739785

# The input is taken from: https://adventofcode.com/2021/day/21/input
task_input = list(load_input_file('input.21.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: list[str]) -> int:
    player1, player2 = parse(task_input)

    three_roles_3d = list(product([1, 2, 3], repeat=3))
    wins = [0, 0]
    score_table = defaultdict(int)
    score_table[(player1, player2), (0, 0), 0] = 1

    while score_table:
        new_score_table = defaultdict(int)
        for (players_position, players_score, turn), universe_number in score_table.items():
            for d1, d2, d3 in three_roles_3d:
                current_player_postion = move_player(players_position[turn], d1)
                current_player_postion = move_player(current_player_postion, d2)
                current_player_postion = move_player(current_player_postion, d3)

                new_players_position = (current_player_postion, players_position[1]) if turn == 0 else (players_position[0], current_player_postion)
                new_players_score = (current_player_postion + players_score[0], players_score[1]) if turn == 0 else (players_score[0], current_player_postion + players_score[1])

                if new_players_score[turn] >= 21:
                    wins[turn] += universe_number
                else:
                    new_score_table[new_players_position, new_players_score, (turn + 1) % 2] += universe_number

        score_table = new_score_table

    return max(wins)


assert solution_for_second_part(example_input) == 444356092776315
print("Solution for the second part:", solution_for_second_part(task_input))
