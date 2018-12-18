UNKNOWN = 0
TREES = 1
OPEN_GROUND = 2
LUMBERJACK = 3


def parse_input(lines: [str]):
    result = {}
    _map = {
        '|': TREES,
        '.': OPEN_GROUND,
        '#': LUMBERJACK
    }

    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            result[(x, y)] = _map[ch]

    return result


def find_all_neighbours(point):
    return [(xi + point[0], yi + point[1]) for xi in [-1, 0, +1] for yi in [-1, 0, 1] if yi != 0 or xi != 0]


def run_turn(state: {}):
    result = {}

    for point, area in state.items():
        neighbor_areas = [state.get(p, UNKNOWN) for p in find_all_neighbours(point)]

        if area == OPEN_GROUND:
            result[point] = TREES if neighbor_areas.count(TREES) >= 3 else OPEN_GROUND
        elif area == TREES:
            result[point] = LUMBERJACK if neighbor_areas.count(LUMBERJACK) >= 3 else TREES
        elif area == LUMBERJACK:
            result[point] = LUMBERJACK if neighbor_areas.count(LUMBERJACK) >= 1 and neighbor_areas.count(TREES) >= 1 else OPEN_GROUND
        else:
            result[point] = state[point]

    return result


def turn_generator(initial_state):
    state = initial_state

    while True:
        state = run_turn(state)
        state_values = list(state.values())
        yield state_values.count(LUMBERJACK) * state_values.count(TREES)


def solution_to_first_part(initial_state):
    generator = turn_generator(initial_state)

    for _, result in zip(range(10), generator):
        pass

    return result


def read_file(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


test_input = parse_input('''.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.'''.splitlines())


assert solution_to_first_part(test_input) == 1147

# Input taken from: https://adventofcode.com/2018/day/18/input
print("Solution for first part:", solution_to_first_part(parse_input(read_file('input.18.txt'))))


previouse_values = [result for _, result in zip(range(1000), turn_generator(parse_input(read_file('input.18.txt'))))]
cycle_start = previouse_values.index(previouse_values[-1])
while True:
    if previouse_values.count(previouse_values[cycle_start - 1]) > 3:
        cycle_start -= 1
    else:
        break

cycle_lenght = previouse_values.index(previouse_values[cycle_start], cycle_start + 1) - cycle_start

print("Solution for second part:", previouse_values[cycle_start - 1 + (1000000000 - cycle_start) % cycle_lenght])
