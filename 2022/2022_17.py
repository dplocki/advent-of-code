from typing import Generator, Iterable, Tuple
import itertools


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def str_to_point_set(rock_shape: str) -> Tuple[set, int, int]:
    result = set((row, column)
        for row, line in enumerate(rock_shape.splitlines())
        for column, character in enumerate(line.strip()) if character == '#')

    xs = [x for _, x in result]
    ys = [y for y, _ in result]
    max_x = max(xs)
    max_y = max(ys)
    min_x = min(xs)
    min_y = min(ys)

    return result, max_x - min_x + 1, max_y - min_y + 1


def simulate_felling_rock(wind_generator: Generator[int, None, None], current_rock, current_shape: set) -> Tuple[int, set]:
    while True:
        wind_index, wind_direction = next(wind_generator)
        move = 0

        # wind move
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
            return current_shape | current_rock, current_shape_bottom, wind_index, 
        else:
            current_rock = tmp


def simulate_falling_rocks(wind: int) -> Generator[Tuple[int, int, int], None, None]:
    wind_generator = itertools.cycle(enumerate(wind))
    rocks = itertools.cycle((index, *str_to_point_set(rock)) for index, rock in enumerate([
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
    ]))

    bottom = 0
    current_shape = set((0, i) for i in range(7))

    while True:
        rock_index, new_rock, _, height = next(rocks)
        starting_row = bottom - 3 - height
        starting_column = 2

        current_rock = set((row + starting_row, column + starting_column) for row, column in new_rock)
        current_shape, current_shape_bottom, wind_index = simulate_felling_rock(wind_generator, current_rock, current_shape)
        bottom = min(current_shape_bottom, bottom)

        yield abs(bottom), rock_index, wind_index


def solution_for_first_part(task_input: Iterable[str]) -> int:
    for (bottom, _, _), _ in zip(simulate_falling_rocks(task_input), range(2022)):
        pass

    return bottom


example_input = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'

assert solution_for_first_part(example_input) == 3068

# # The input is taken from: https://adventofcode.com/2022/day/17/input
task_input = load_input_file('input.17.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


def floyd(values) -> Tuple[int, int]:
    index = 0
    while values[index] != values[index * 2]:
        index += 1
   
    cycle_start = 0
    hare_index = index
    tortoise_index = 0
    while values[tortoise_index] != values[hare_index]:
        hare_index += 1
        tortoise_index += 1
        cycle_start += 1
 
    cycle_length = 1
    hare_index = tortoise_index + 1
    while values[tortoise_index] != values[hare_index]:
        hare_index += 1
        cycle_length += 1

    return cycle_length, cycle_start


def solution_for_second_part(task_input: Iterable[str]) -> int:
    bottom_values = {}
    indexes_cache = {}
    simulator = simulate_falling_rocks(task_input)
    index = 0
    seek_index = 1_000_000_000_000

    while True:
        bottom, rock_index, wind_index = next(simulator)
        previous_values = tuple((r, w) for i, (r, w, _) in enumerate(indexes_cache.keys()) if i > index - 4)

        if (rock_index, wind_index, previous_values) in indexes_cache:
            prev_index, prev_bottom = indexes_cache[rock_index, wind_index, previous_values]
            cycle_length = index - prev_index
            cycle_start = prev_index

            return ((seek_index - cycle_start) // cycle_length) * (bottom - prev_bottom) \
                + bottom_values[cycle_start + (seek_index - cycle_start - 1) % cycle_length]
        else:
            indexes_cache[rock_index, wind_index, previous_values] = (index, bottom)
            bottom_values[index] = bottom

        index += 1


assert solution_for_second_part(example_input) == 1514285714288
print("Solution for the second part:", solution_for_second_part(task_input))
