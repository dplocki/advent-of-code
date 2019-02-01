SIZE = 100


def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def input_into_state(lines: [str]):
    result = set()

    y = 0
    for line in lines:
        for x, value in enumerate(line):
            if value == '#':
                result.add((x,y))
        y += 1

    return result


def run_state_100_time(first_generation: set, adjust_state) -> int:


    def get_neighbours(state: set, point: tuple) -> int:
        neighbours = [
                (xi + point[0], yi + point[1])
                for xi in [-1, 0, 1]
                for yi in [-1, 0, 1]
                if yi != 0 or xi != 0
            ]

        return sum(1 for p in neighbours if p in state)


    def build_new_state(old_state: set) -> set:
        new_state = set()
        for y in range(SIZE):
            for x in range(SIZE):
                point = (x, y)
                number_of_neiborns = get_neighbours(old_state, point)
                if number_of_neiborns == 3 or (point in old_state and number_of_neiborns == 2):
                    new_state.add(point)

        return new_state


    state = adjust_state(first_generation)
    for _ in range(100):
        state = adjust_state(build_new_state(state))

    return len(state)


def solution_for_first_part(first_generation: set):
    return run_state_100_time(first_generation, lambda x: x)


def solution_for_second_part(first_generation: set):


    def lights_corners(state: set):
        state.add((0, 0))
        state.add((0, 99))
        state.add((99, 0))
        state.add((99, 99))

        return state


    return run_state_100_time(first_generation, lights_corners)


# The solution is taken from: https://adventofcode.com/2015/day/18/input
first_generation = input_into_state(load_input_file('input.18.txt'))
print("Solution for the first part:", solution_for_first_part(first_generation))
print("Solution for the second part:", solution_for_second_part(first_generation))
