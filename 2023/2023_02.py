from typing import Callable, Generator, Iterable


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(line: str) -> bool:
    result = {}

    tokens = line.split(':')
    result['id'] = int(tokens[0].split(' ')[1])
    result['green'] = []
    result['red'] = []
    result['blue'] = []

    for subsets in tokens[1].split(';'):
        cubes_tokens = subsets.split(',')

        for c in cubes_tokens:
            c = c.strip()
            n, name = c.split(' ')
            n = int(n)

            result[name].append(n)

    return result


def internal_logic_for_first_part(game_object: dict):
    # possible if the bag had been loaded with only 12 red cubes, 13 green cubes, and 14 blue cubes
    if any(e > 12 for e in game_object['red']) or \
        any(e > 13 for e in game_object['green']) or \
        any(e > 14 for e in game_object['blue']):
        return 0

    return game_object['id']


def solution(task_input: Iterable[str], internal_logic: Callable[[str], int]) -> int:
    return sum(map(internal_logic, map(parse, task_input)))


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return solution(task_input, internal_logic_for_first_part)


example_input = '''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'''.splitlines()

assert solution_for_first_part(example_input) == 8

# The input is taken from: https://adventofcode.com/2023/day/2/input
task_input = list(load_input_file('input.02.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def internal_logic_for_second_part(game_object: dict) -> int:
    return max(game_object['red']) * max(game_object['green']) * max(game_object['blue'])


def solution_for_second_part(task_input: Iterable[str]) -> int:
    return solution(task_input, internal_logic_for_second_part)


assert solution_for_second_part(example_input) == 2286

print("Solution for the second part:", solution_for_second_part(task_input))