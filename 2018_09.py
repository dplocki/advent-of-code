def board_generator():
    board = [0]
    current_marble = 1
    current_marble_index = 0

    while True:
        board_lenght = len(board)
        removed = []

        if current_marble % 23 != 0:
            current_marble_index = (current_marble_index + 1) % board_lenght + 1
            if current_marble_index > board_lenght:
                board.append(current_marble)
            else:
                board.insert(current_marble_index, current_marble)
        else:
            removed.append(current_marble)
            removed.append(board[current_marble_index - 7])
            del board[current_marble_index - 7]

            current_marble_index = (current_marble_index - 7) % board_lenght

        yield current_marble, board, removed
        current_marble += 1


def test_of_board(generator, expected_current_marble, expected_board, expected_removed = []):
    current_marble, board, removed = next(generator)

    assert current_marble == expected_current_marble, f"Recived: {current_marble} Expected: {expected_current_marble}"
    assert board == expected_board, f"Recived: {board} Expected: {expected_board}"
    assert removed == expected_removed, f"Recived: {removed} Expected: {expected_removed}"


turn = board_generator()
test_of_board(turn, 1, [0, 1])
test_of_board(turn, 2, [0, 2, 1])
test_of_board(turn, 3, [0, 2, 1, 3])
test_of_board(turn, 4, [0, 4, 2, 1, 3])
test_of_board(turn, 5, [0, 4, 2, 5, 1, 3])
test_of_board(turn, 6, [0, 4, 2, 5, 1, 6, 3])

turn = board_generator()
[_ for _ in zip(turn, range(21))]
test_of_board(turn, 23, [0, 16, 8, 17, 4, 18, 19, 2, 20, 10, 21, 5, 22, 11, 1, 12, 6, 13, 3, 14, 7, 15], [23, 9])


def play(player_count, last_marble):
    player_scores = [0] * player_count
    
    for current_marble, _, removed in board_generator():
        player_scores[current_marble % player_count] += sum(removed)
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
