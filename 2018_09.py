from collections import deque


def board_generator():
    board = deque([0])
    current_marble = 1
    removed = None

    while True:
        if current_marble % 23 != 0:
            board.rotate(-1)
            board.append(current_marble)
            removed = None
        else:
            board.rotate(7)
            removed = board.pop()
            board.rotate(-1)

        yield current_marble, removed
        current_marble += 1


def test_of_board(generator, expected_current_marble, expected_removed = None):
    current_marble, removed = next(generator)

    assert current_marble == expected_current_marble, f"Recived: {current_marble} Expected: {expected_current_marble}"
    assert removed == expected_removed, f"Recived: {removed} Expected: {expected_removed}"


turn = board_generator()
test_of_board(turn, 1)
test_of_board(turn, 2)
test_of_board(turn, 3)
test_of_board(turn, 4)
test_of_board(turn, 5)
test_of_board(turn, 6)

turn = board_generator()
[_ for _ in zip(turn, range(21))]
test_of_board(turn, 23, 9)


def play(player_count, last_marble):
    player_scores = [0] * player_count
    
    for current_marble, removed in board_generator():
        if removed:
            player_scores[current_marble % player_count] += removed + current_marble

        if current_marble == last_marble:
            return player_scores


def test_play(player_count, last_marble, excepted_high_score):
    result = max(play(player_count, last_marble))

    assert result == excepted_high_score, f"Recived: {result}, Expected: {excepted_high_score}"


test_play(9, 25, 32)
test_play(10, 1618, 8317)
test_play(13, 7999, 146373)
test_play(17, 1104, 2764)
test_play(21, 6111, 54718)
test_play(30, 5807, 37305)

print('Solution for first part:', max(play(424, 71144)))
print('Solution for second part:', max(play(424, 71144 * 100)))
