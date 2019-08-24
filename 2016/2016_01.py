NORTH = 0
SOUTH = 2
WEST = 3
EAST = 1


def load_input_file(file_name: str):
    with open(file_name) as file:
        return file.read()

def parse(input: str):

    def split_to_lines(input: str):
        yield from input.split(", ")

    for line in split_to_lines(input):
        yield line[0], int(line[1:])


def solution_for_first_part(input: str) -> int:
    move_matrix = {
        NORTH: (0, 1),
        SOUTH: (0, -1),
        WEST: (-1, 0),
        EAST: (1, 0)
    }
    face = NORTH
    coordinates = (0, 0)
    for turn, steps in parse(input):
        face = (face + (1 if turn == 'R' else -1)) % 4

        move_to = move_matrix[face]
        coordinates = (coordinates[0] + move_to[0] * steps, coordinates[1] + move_to[1] * steps)

    return abs(coordinates[0]) + abs(coordinates[1])


assert solution_for_first_part('R2, L3') == 5
assert solution_for_first_part('R2, R2, R2') == 2
assert solution_for_first_part('R5, L5, R5, R3') == 12


# The input is taken from: https://adventofcode.com/2016/day/1/input
print("Solution for the first part:", solution_for_first_part(load_input_file('input.01.txt')))
