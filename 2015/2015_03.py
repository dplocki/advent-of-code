COORDINATE_HASH_MAP = {
    '>': (1, 0),
    '<': (-1, 0),
    '^': (0, -1),
    'v': (0, 1)
}


def load_input_file(file_name):
    with open(file_name) as file:
        return file.read()


def move(current_position, coordinate):
    correction = COORDINATE_HASH_MAP[coordinate]
    return (current_position[0] + correction[0], current_position[1] + correction[1])


def solution_to_the_first_part(coordinates: str):
    houses = set()
    current_position = (0, 0)

    for coordinate in coordinates:
        houses.add(current_position)

        current_position = move(current_position, coordinate)

    return len(houses)


def solution_to_the_second_part(coordinates: str):
    houses = set()

    current_santa = (0, 0)
    waiting_santa = (0, 0)
   
    for coordinate in coordinates:
        houses.add(current_santa)
        
        current_santa = move(current_santa, coordinate)

        current_santa, waiting_santa = waiting_santa, current_santa

    return len(houses)


# The input is taken from: https://adventofcode.com/2015/day/3/input
task_input = load_input_file('input.03.txt')
print("Solution for the first part:", solution_to_the_first_part(task_input))
print("Solution for the second part:", solution_to_the_second_part(task_input))
