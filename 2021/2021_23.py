from queue import PriorityQueue


AMPHIPOD_TYPE = 0
X = 1
Y = 2

ROOMS_X = { 'A': 3, 'B': 5, 'C': 7, 'D': 9 }
MOVE_COST = { 'A': 1, 'B': 10, 'C': 100, 'D': 1000 }
REQUIRED_POSITIONS = (('A', 3, 2), ('A', 3, 3), ('B', 5, 2), ('B', 5, 3), ('C', 7, 2), ('C', 7, 3), ('D', 9, 2), ('D', 9, 3))


def load_input_file(file_name: str) -> list[str]:
    with open(file_name) as file:
        yield from (line for line in file)


def parse(task_input: list[str]) -> tuple[int, int, str]:
    for r, line in enumerate(task_input):
        for c, v in enumerate(line):
            yield c, r, v


def move(amphipods: tuple[tuple[str, int, int]], amphipod: tuple[str, int, int], new_position: tuple[int, int]) -> tuple[str, int, int]:
    px, py = new_position
    result = [(amphipod_type, x, y) for amphipod_type, x, y in amphipods if x != amphipod[X] or y != amphipod[Y]]
    result.append((amphipod[AMPHIPOD_TYPE], px, py))
    result.sort()

    return tuple(result)


def positions_in_hallway(amphipods: tuple[tuple[str, int, int]], start: tuple[int, int]) -> list[tuple[int, int]]:
    x_in_hallway = {x for _, x, _ in amphipods}
    rooms_x = ROOMS_X.values()

    x = start
    while x > 1:
        x -= 1

        if x in x_in_hallway:
            break

        if x in rooms_x:
            continue

        yield (x, 1)

    x = start
    while x < 11:
        x += 1

        if x in x_in_hallway:
            break

        if x in rooms_x:
            continue

        yield (x, 1)


def is_path_blocked(start_x: int, end_x: int, amphipods_in_hallway: list[tuple[tuple[str, int, int]]]) -> bool:
    from_x = min(start_x, end_x)
    to_x = max(start_x, end_x)
    result = any(from_x < x < to_x for _, x, _ in amphipods_in_hallway)
    return result


def get_room_occupant(amphipods: list[tuple[tuple[str, int, int]]], amphipod_type: str) -> list[tuple[tuple[str, int, int]]]:
    return [amphipod for amphipod in amphipods if amphipod[X] == ROOMS_X[amphipod_type]]


def is_anybody_on_position(amphipods: list[tuple[tuple[str, int, int]]], position: tuple[int, int]) -> bool:
    px, py = position
    result = sum(1 for _, x, y in amphipods if x == px and y == py)
    return result != 0


def produce_new_positions_sets(amphipods: list[tuple[tuple[str, int, int]]]) -> tuple[int, tuple[tuple[str, int, int]]]:
    amphipods_in_hallway = [amphipod for amphipod in amphipods if amphipod[Y] == 1]
    for amphipod_type, x, y in amphipods_in_hallway:
        if is_path_blocked(x, ROOMS_X[amphipod_type], amphipods_in_hallway):
            continue

        room_mates = get_room_occupant(amphipods, amphipod_type)  
        room_mates_number = len(room_mates)
        if room_mates_number == 0 or (room_mates_number == 1 and room_mates[0][AMPHIPOD_TYPE] == amphipod_type):
            cost_move = MOVE_COST[amphipod_type] * (abs(x - ROOMS_X[amphipod_type]) + (2 if room_mates_number == 0 else 1))
            yield cost_move, move(amphipods, (amphipod_type, x, y), (ROOMS_X[amphipod_type], (3 if room_mates_number == 0 else 2)))

    for amphipod_type, x, y in amphipods:
        if y != 2:
            continue

        if x == ROOMS_X[amphipod_type]:
            if any(amphipod for amphipod in amphipods if amphipod[X] == ROOMS_X[amphipod_type] and amphipod[AMPHIPOD_TYPE] != amphipod_type) == 0:
                continue

        for position in positions_in_hallway(amphipods_in_hallway, x):
            yield MOVE_COST[amphipod_type] * (1 + abs(position[0] - x)), move(amphipods, (amphipod_type, x, y), position)

    for amphipod_type, x, y in amphipods:
        if y != 3:
            continue

        if x == ROOMS_X[amphipod_type]:
            continue

        if is_anybody_on_position(amphipods, (x, 2)):
            continue

        for position in positions_in_hallway(amphipods_in_hallway, x):
            yield MOVE_COST[amphipod_type] * (2 + abs(position[0] - x)), move(amphipods, (amphipod_type, x, y), position)


def read_amphipods_positions(raw_map: list[tuple[int, int, str]]) -> tuple[tuple[str, int, int]]:
    result = sorted((value, x, y) for x, y, value in raw_map if value in 'ABCD')
    return tuple(result)


def solution_for_first_part(task_input: list[str]) -> int:
    amphipods = read_amphipods_positions(parse(task_input))

    frontier = PriorityQueue()
    frontier.put((0, amphipods))

    cost_so_far = {amphipods: 0}

    while not frontier.empty():
        current_postions = frontier.get()[1]
        if current_postions == REQUIRED_POSITIONS:
            return cost_so_far[current_postions]

        for cost_of_move, next in produce_new_positions_sets(current_postions):
            cost_of_move += cost_so_far[current_postions]

            if next not in cost_so_far or cost_of_move < cost_so_far[next]:
                cost_so_far[next] = cost_of_move
                priority = cost_of_move
                frontier.put((priority, next))

    raise Exception('Path not found')


example_input = '''#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
'''.splitlines()

assert solution_for_first_part(example_input) == 12521

# The input is taken from: https://adventofcode.com/2021/day/23/input
task_input = list(load_input_file('input.23.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
