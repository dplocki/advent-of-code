from queue import PriorityQueue
from typing import Callable


AMPHIPOD_TYPE = 0
X = 1
Y = 2

ROOMS_X = { 'A': 3, 'B': 5, 'C': 7, 'D': 9 }
MOVE_COST = { 'A': 1, 'B': 10, 'C': 100, 'D': 1000 }


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


def positions_in_hallway(x_in_hallway: set[int], start: tuple[int, int]) -> list[tuple[int, int]]:
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


def is_path_blocked(start_x: int, end_x: int, amphipods_in_hallway: set[int]) -> bool:
    from_x = min(start_x, end_x)
    to_x = max(start_x, end_x)
    result = any(from_x < x < to_x for x in amphipods_in_hallway)
    return result


def get_position_in_room(amphipods: list[tuple[tuple[str, int, int]]], amphipod_type: str, room_deep: int) -> list[tuple[tuple[str, int, int]]]:
    occupants_number = 0

    for type, x, _ in amphipods:
        if x != ROOMS_X[amphipod_type]:
            continue

        if type != amphipod_type:
            return 0

        occupants_number += 1

    return room_deep - occupants_number


def is_anybody_on_position(amphipods: list[tuple[tuple[str, int, int]]], position: tuple[int, int]) -> bool:
    px, py = position
    result = sum(1 for _, x, y in amphipods if x == px and y == py)
    return result != 0


def produce_new_positions_sets(amphipods: list[tuple[tuple[str, int, int]]], rooms_deep: int) -> tuple[int, tuple[tuple[str, int, int]]]:
    amphipods_x_in_hallway = {x for _, x, y in amphipods if y == 1}

    for amphipod_type, x, y in amphipods:
        if y == 1:
            if is_path_blocked(x, ROOMS_X[amphipod_type], amphipods_x_in_hallway):
                continue

            steps_in_room = get_position_in_room(amphipods, amphipod_type, rooms_deep)
            if steps_in_room != 0:
                cost_move = MOVE_COST[amphipod_type] * (abs(x - ROOMS_X[amphipod_type]) + steps_in_room)
                yield cost_move, move(amphipods, (amphipod_type, x, y), (ROOMS_X[amphipod_type], 1 + steps_in_room))
        else:
            if is_anybody_on_position(amphipods, (x, y - 1)):
                continue

            if x == ROOMS_X[amphipod_type]:
                if not any(amphipod for amphipod in amphipods if amphipod[X] == ROOMS_X[amphipod_type] and amphipod[AMPHIPOD_TYPE] != amphipod_type):
                    continue

            for position in positions_in_hallway(amphipods_x_in_hallway, x):
                cost_move = MOVE_COST[amphipod_type] * ((y - 1) + abs(position[0] - x))
                yield cost_move, move(amphipods, (amphipod_type, x, y), position)


def read_amphipods_positions(raw_map: list[tuple[int, int, str]]) -> tuple[tuple[str, int, int]]:
    result = sorted((value, x, y) for x, y, value in raw_map if value in 'ABCD')
    return tuple(result)


def find_the_way(task_input: list[str], is_end: Callable, heuristic: Callable, rooms_deep: int) -> int:
    amphipods = read_amphipods_positions(parse(task_input))

    frontier = PriorityQueue()
    frontier.put((0, amphipods))

    cost_so_far = { amphipods: 0 }

    while not frontier.empty():
        current_postions = frontier.get()[1]
        if is_end(current_postions):
            return cost_so_far[current_postions]

        for cost_of_move, next in produce_new_positions_sets(current_postions, rooms_deep):
            cost_of_move += cost_so_far[current_postions]

            if next not in cost_so_far or cost_of_move < cost_so_far[next]:
                cost_so_far[next] = cost_of_move
                priority = cost_of_move + heuristic(next)
                frontier.put((priority, next))

    raise Exception('Path not found')


def solution_for_first_part(task_input: list[str]) -> int:
    ROOM_DEEP = 2
    REQUIRED_POSITIONS_FIRST_PART = (('A', 3, 2), ('A', 3, 3), ('B', 5, 2), ('B', 5, 3), ('C', 7, 2), ('C', 7, 3), ('D', 9, 2), ('D', 9, 3))

    def is_end(current_positions):
        return current_positions == REQUIRED_POSITIONS_FIRST_PART

    def heuristic(positions: tuple[tuple[str, int, int]]) -> int:
        return sum(abs(r[1] - c[1]) + abs(r[2] - c[2]) for r, c in zip(REQUIRED_POSITIONS_FIRST_PART, positions))

    return find_the_way(task_input, is_end, heuristic, ROOM_DEEP)


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


def solution_for_second_part(task_input: list[str]) -> int:
    ADDITIONAL_LINES = ['  #D#C#B#A#', '  #D#B#A#C#']
    REQUIRED_POSITIONS_SECOND_PART = (
        ('A', 3, 2), ('A', 3, 3), ('A', 3, 4), ('A', 3, 5),
        ('B', 5, 2), ('B', 5, 3), ('B', 5, 4), ('B', 5, 5),
        ('C', 7, 2), ('C', 7, 3), ('C', 7, 4), ('C', 7, 5),
        ('D', 9, 2), ('D', 9, 3), ('D', 9, 4), ('D', 9, 5))

    task_input = task_input[:3] + ADDITIONAL_LINES + task_input[3:]

    def is_end(current_positions):
        return current_positions == REQUIRED_POSITIONS_SECOND_PART

    def heuristic(positions: tuple[tuple[str, int, int]]) -> int:
        return sum(abs(r[1] - c[1]) + abs(r[2] - c[2]) for r, c in zip(REQUIRED_POSITIONS_SECOND_PART, positions))

    return find_the_way(task_input, is_end, heuristic, 4)


assert solution_for_second_part(example_input) == 44169
print("Solution for the second part:", solution_for_second_part(task_input))
