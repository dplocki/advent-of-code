def load_input_file(file_name: str):
    with open(file_name) as file:
        return file.read()

def parse(input: str):

    def split_to_lines(input: str):
        yield from input.split(", ")

    for line in split_to_lines(input):
        yield line[0], int(line[1:])


def walk_on_path(input: str):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

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

        for _ in range(steps):
            coordinates = (coordinates[0] + move_to[0], coordinates[1] + move_to[1])
            yield coordinates


def blocks_away(coordinates) -> int:
    return abs(coordinates[0]) + abs(coordinates[1])


def solution_for_first_part(input: str) -> int:
    for coordinates in walk_on_path(input):
        pass

    return blocks_away(coordinates)


assert solution_for_first_part('R2, L3') == 5
assert solution_for_first_part('R2, R2, R2') == 2
assert solution_for_first_part('R5, L5, R5, R3') == 12


def solution_for_second_part(input: str) -> int:
    visted_places = set()
    for coordinates in walk_on_path(input):
        if coordinates in visted_places:
            return blocks_away(coordinates)

        visted_places.add(coordinates)

    return None


assert solution_for_second_part('R8, R4, R4, R8') == 4


# The input is taken from: https://adventofcode.com/2016/day/1/input
input = load_input_file('input.01.txt')
print("Solution for the first part:", solution_for_first_part(input))
print("Solution for the second part:", solution_for_second_part(input))
