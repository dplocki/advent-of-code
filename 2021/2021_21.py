CIRCLE_SIZE = 10


def load_input_file(file_name: str) -> list[str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: list[str]) -> tuple[int, int]:
    return tuple(int(line[-1]) for line in task_input)


def die_roll() -> list[tuple[int, int]]:
    use_count = 1
    while True:
        for value in range(100):
            yield value + 1, use_count
            use_count += 1


def move_player(start: int, how_much: int) -> int:
    return ((start - 1 + how_much) % CIRCLE_SIZE) + 1


def solution_for_first_part(task_input: list[str]) -> int:
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
task_input = load_input_file('input.21.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
