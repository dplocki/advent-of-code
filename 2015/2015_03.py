def load_input_file(file_name):
    with open(file_name) as file:
        return file.read()


def solution_to_the_first_part(coordinates: str):
    coordinate_hash = {
        '>': (1, 0),
        '<': (-1, 0),
        '^': (0, -1),
        'v': (0, 1)
    }

    houses = set()
    current_position = (0,0)
    for coordinate in coordinates:
        houses.add(current_position)

        correction = coordinate_hash[coordinate]
        current_position = (current_position[0] + correction[0], current_position[1] + correction[1])

    return len(houses)


# The solution is taken from: https://adventofcode.com/2015/day/3/input
print("Solution for the first part:", solution_to_the_first_part(load_input_file('input.03.txt')))
