WALL = 0
FLOOR = 1
OXYGEN_SYSTEM = 2
END_OPTCODE = 99


def load_input_file(file_name: str):
    with open(file_name) as file:
        return [int(x) for x in file.read().split(',')]


def run_program(memory: dict, outside, index=0, relative_base=0) -> []:

    def from_memory(memory, paramater, relative_base):
        index, mode = paramater

        # position mode
        if mode == 0:
            return memory.get(memory[index], 0)
        # immediate mode
        elif mode == 1:
            return memory.get(index, 0)
        # relative mode
        elif mode == 2:
            return memory.get(relative_base + memory[index], 0)
        else:
            raise Exception(f'Uknown mode: {mode}')

    def to_memory(memory, paramater, value, relative_base):
        index, mode = paramater

        new_index = None
        # position mode
        if mode == 0:
            new_index = memory[index]
        # immediate mode
        elif mode == 1:
            new_index = index
        # relative mode
        elif mode == 2:
            new_index = relative_base + memory[index]
        else:
            raise Exception(f'Uknown mode: {mode}')

        memory[new_index] = value

    while True:
        cmd = memory[index]

        optcode = cmd % 100
        first_parameter = (index + 1, (cmd // 100) % 10)
        second_parameter = (index + 2, (cmd // 1000) % 10)
        third_parameter = (index + 3, (cmd // 10000) % 10)

        if optcode == END_OPTCODE:
            return None, index, memory, relative_base

        # Calculation
        elif optcode == 1: # adding
            to_memory(
                memory,
                third_parameter,
                from_memory(memory, first_parameter, relative_base) + from_memory(memory, second_parameter, relative_base),
                relative_base
            )
            index += 4

        elif optcode == 2: # multiplication
            to_memory(
                memory,
                third_parameter,
                from_memory(memory, first_parameter, relative_base) * from_memory(memory, second_parameter, relative_base),
                relative_base
            )
            index += 4

        # I/O operations
        elif optcode == 3:
            to_memory(memory, first_parameter, outside.pop(0), relative_base)
            index += 2

        elif optcode == 4:
            index += 2
            return from_memory(memory, first_parameter, relative_base), index, memory, relative_base

        # Jumps
        elif optcode == 5: # jump-if-true
            index = from_memory(memory, second_parameter, relative_base) if from_memory(memory, first_parameter, relative_base) != 0 else index + 3

        elif optcode == 6: # jump-if-false
            index = from_memory(memory, second_parameter, relative_base) if from_memory(memory, first_parameter, relative_base) == 0 else index + 3

        # Save in memory operations
        elif optcode == 7: # less than
            to_memory(
                memory,
                third_parameter,
                1 if from_memory(memory, first_parameter, relative_base) < from_memory(memory, second_parameter, relative_base) else 0,
                relative_base
            )
            index += 4

        elif optcode == 8: # equals
            to_memory(
                memory,
                third_parameter,
                1 if from_memory(memory, first_parameter, relative_base) == from_memory(memory, second_parameter, relative_base) else 0, relative_base
            )
            index += 4

        # Adjust the relative base
        elif optcode == 9:
            relative_base += from_memory(memory, first_parameter, relative_base)
            index += 2

        else:
            raise Exception(f'Unknown opcode: "{cmd}"')


def directory_to_coordinates(x: int, y: int, directory: int) -> tuple:
    if directory == 1:
        return (x, y - 1)
    elif directory == 2:
        return (x, y + 1)
    elif directory == 3:
        return (x - 1, y)
    elif directory == 4:
        return (x + 1, y)


def get_surranding(x: int, y: int) -> dict:
    return {(x, y - 1): 1,
            (x, y + 1): 2,
            (x - 1, y): 3,
            (x + 1, y): 4}


def bfs_abstract(starting_possibilites, found, append, maze_map: dict):
    possiblities = starting_possibilites

    visited = set()
    while possiblities:
        point, metadata = possiblities.pop(0)
        if found(point):
            return metadata

        visited.add(point)
        for p in [(point[0], point[1] - 1), (point[0], point[1] + 1), (point[0] - 1, point[1]), (point[0] + 1, point[1])]:
            if (p in visited) or (p in maze_map and maze_map[p] == WALL):
                continue

            possiblities.append(append(p, metadata))


def find_near_unknown(maze_map: dict, x: int, y: int) -> int:

    def found(point):
        return not point in maze_map

    def append(point, direction):
        return (point, direction)

    return bfs_abstract(
            [(p, d) for p,d in get_surranding(x, y).items() if maze_map[p] != WALL],
            found,
            append,
            maze_map
        )


def choose_direction(maze_map, x, y, direction, previous_x, previous_y):
    directions = [d for p, d in get_surranding(x, y).items() if not p in maze_map]
    return directions[0] if directions else find_near_unknown(maze_map, x, y)


def run_program_to_end(memory: {}):
    memory = {i:v for i, v in enumerate(memory)}
    position_of_oxygen_system = None
    index, relative_base = 0, 0
    maze_map = {(0, 0): 1}
    direction = 1
    x, y, previous_x, previous_y = 0, 0, 0, 0

    while memory[index] != END_OPTCODE:
        direction = choose_direction(maze_map, x, y, direction, previous_x, previous_y)
        if direction == None:
            return maze_map, position_of_oxygen_system

        previous_x, previous_y = x, y
        x, y = directory_to_coordinates(x, y, direction)
        output, index, memory, relative_base = run_program(memory, [direction], index, relative_base)

        maze_map[(x, y)] = output
        if output == WALL:
            x, y = previous_x, previous_y
        elif output == OXYGEN_SYSTEM:
            position_of_oxygen_system = x, y


def find_path_size_to(maze_map, end_point):

    def found(point):
        return point == end_point

    def append(point, steps):
        return (point, steps + 1)

    return bfs_abstract(
            [((0, 0), 0)],
            found,
            append,
            maze_map
        )


def solution_for_first_part(task_input: [int]):
    return find_path_size_to(*run_program_to_end(task_input))

# The input is taken from: https://adventofcode.com/2019/day/15/input
task_input = list(load_input_file('input.15.txt'))

print("Solution for the first part:", solution_for_first_part(task_input))
