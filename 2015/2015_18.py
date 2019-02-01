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


def get_neighbours(state: set, point: tuple) -> int:
    neighbours = [(xi + point[0], yi + point[1]) for xi in [-1, 0, +1] for yi in [-1, 0, 1] if yi != 0 or xi != 0]
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


def state_after_100_runs(first_generation: set):
    state = first_generation
    for _ in range(100):
        state = build_new_state(state)

    return state


# The solution is taken from: https://adventofcode.com/2015/day/18/input
print("Solution for the first part:", len(state_after_100_runs(input_into_state(load_input_file('input.18.txt')))))
