from typing import Generator, Iterable


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def game_fits(game: str) -> bool:
    for s in game.split(';'):

        cubes = s.split(',')

        for c in cubes:
            c = c.strip()
            n, name = c.split(' ')
            n = int(n)

            if name == 'red' and n > 12:
                return False


            if name == 'green' and n > 13:
                return False


            if name == 'blue' and n > 14:
                return False

    return True


def solution_for_first_part(task_input: Iterable[str]) -> int:
    result = 0

    for line in task_input:
        tokens = line.split(':')
        game = tokens[1]
        game_id = int(tokens[0].split(' ')[1])

        if game_fits(game):
            result += game_id

    return result


example_input = '''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'''.splitlines()

assert solution_for_first_part(example_input) == 8

# The input is taken from: https://adventofcode.com/2023/day/2/input
task_input = list(load_input_file('input.02.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
