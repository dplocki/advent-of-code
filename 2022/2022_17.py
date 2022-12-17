from typing import Generator, Iterable, Tuple
import itertools


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def str_to_point_set(rock_shape: str) -> Tuple[set, int, int]:
    result = set((row, column)
        for row, line in enumerate(rock_shape.splitlines())
        for column, character in enumerate(line) if character == '#')

    xs = [x for _, x in result]
    ys = [y for y, _ in result]
    max_x = max(xs)
    max_y = max(ys)
    min_x = min(xs)
    min_y = min(ys)

    return result, max_x - min_x + 1, max_y - min_y + 1


def solution_for_first_part(task_input: Iterable[str]) -> int:


    def simulate_felling_rock(wind_generator: Generator[int, None, None], current_rock, current_shape: set) -> Tuple[int, set]:
        while True:
            wind_direction = next(wind_generator)
            move = 0
            xs = set(x for _, x in current_rock)
            if wind_direction == '<' and 0 not in xs:
                move = -1
            elif wind_direction == '>' and 6 not in xs:
                move = 1

            if move != 0:
                tmp = set((row, column + move) for row, column in current_rock)
                if not tmp & current_shape:
                    current_rock = tmp

            # fell down
            tmp = set((row + 1, column) for row, column in current_rock)
            if tmp & current_shape:
                current_shape_bottom = min(y for y, _ in current_rock)
                return min(bottom, current_shape_bottom), current_shape | current_rock
            else:
                current_rock = tmp


    wind_generator = itertools.cycle(task_input)
    rocks = itertools.cycle(str_to_point_set(rock) for rock in [
        '''####''',
        '''.#.
###
.#.''',
        '''..#
..#
###''',
        '''#
#
#
#''',  
        '''##
##'''
    ])

    bottom = 0
    current_shape = set((0, i) for i in range(7))

    for _ in range(2022):
        new_rock, _, height = next(rocks)
        starting_row = bottom - 3 - height
        starting_column = 2

        current_rock = set((row + starting_row, column + starting_column) for row, column in new_rock)
        bottom, current_shape = simulate_felling_rock(wind_generator, current_rock, current_shape)
    
    return abs(bottom)


example_input = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'

assert solution_for_first_part(example_input) == 3068

# The input is taken from: https://adventofcode.com/2022/day/17/input
task_input = load_input_file('input.17.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
