END_OPTCODE = 99


def load_input_file(file_name):
    with open(file_name) as file:
        return [int(x) for x in file.read().split(',')]


def run_program(memory: {}, outside, index=0, relative_base=0) -> []:

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


def run_program_to_end(memory: {}, program_input = None):
    index, relative_base = 0, 0
    program_input = program_input or []

    while memory[index] != END_OPTCODE:
        output, index, memory, relative_base = run_program(memory, program_input, index, relative_base)

        yield output


def get_video_feed(running_program):
    return ''.join([chr(output) for output in running_program if output != None])


def get_scaffold_map(memory):
    memory = {i:v for i, v in enumerate(memory)}

    ascii_view = [line for line in [line.strip() for line in get_video_feed(run_program_to_end(memory)).splitlines()] if line]
    scaffold_map = set()
    vaccum_robot_position = None

    for y, line in enumerate(ascii_view):
        for x, c in enumerate(line):
            if c == '#':
                scaffold_map.add((x, y))
            elif c in '^v<>':
                scaffold_map.add((x, y))
                vaccum_robot_position = (x, y, c)


    return scaffold_map, (len(ascii_view[0]), len(ascii_view)), vaccum_robot_position


def get_intersections(scaffold_map: set, scaffold_map_size):
    max_x, max_y = scaffold_map_size
    return [(x, y)
        for y in range(max_y)
        for x in range(max_x)
        if (x, y) in scaffold_map and (x - 1, y) in scaffold_map and (x + 1, y) in scaffold_map and (x, y - 1) in scaffold_map and (x, y + 1) in scaffold_map]


def solution_for_first_part(scaffold_map: set, scaffold_map_size):
    return sum([x*y for x, y in get_intersections(scaffold_map, scaffold_map_size)])


# The input is taken from: https://adventofcode.com/2019/day/17/input
memory = list(load_input_file('input.17.txt'))
scaffold_map, scaffold_map_size, vaccum_robot_position = get_scaffold_map(memory)
print("Solution for the first part:", solution_for_first_part(scaffold_map, scaffold_map_size))


def solution_for_second_part(memory, scaffold_map: set, vaccum_robot_position: tuple):


    def find_the_path(scaffold_map: set, vaccum_robot_position: tuple):


        def where_turn(x, y, facing, scaffold_map, visited):
            tmp = (x - 1, y)
            if tmp in scaffold_map and not tmp in visited:
                return {
                        '^': ('L', '<'),
                        'v': ('R', '<')
                    }[facing]

            tmp = (x + 1, y)
            if tmp in scaffold_map and not tmp in visited:
                return {
                        '^': ('R', '>'),
                        'v': ('L', '>')
                    }[facing]

            tmp = (x, y - 1)
            if tmp in scaffold_map and not tmp in visited:
                return {
                        '<': ('R', '^'),
                        '>': ('L', '^')
                    }[facing]

            tmp = (x, y + 1)
            if tmp in scaffold_map and not tmp in visited:
                return {
                        '<': ('L', 'v'),
                        '>': ('R', 'v')
                    }[facing]

            return None, facing


        def reformat_path(path):
            steps = 0
            for c in path:
                if c == 'M':
                    steps += 1
                else:
                    if steps > 0:
                        yield str(steps)
                        steps = 0
                    yield c

            if steps > 0:
                yield str(steps)


        visited = set()
        start_x, start_y, facing = vaccum_robot_position
        x, y = start_x, start_y
        path = ''

        while True:
            new_position = {
                'v': (x, y + 1),
                '^': (x, y - 1),
                '<': (x - 1, y),
                '>': (x + 1, y)
            }[facing]

            if new_position in scaffold_map:
                path += 'M'
                visited.add(new_position)
                x, y = new_position
            else:
                instruction, facing = where_turn(x, y, facing, scaffold_map, visited)
                if instruction == None:
                    return ','.join(reformat_path(path))

                path += instruction


    def split_path_to_subfunction(path):

        def get_token(path):
            index = path.index(',')
            token = path[:index]
            if not token.isdigit() or token == '':
                index = path.index(',', index + 1)

            return path[:index], path[index + 1:]

        def get_the_longest(path):
            result, rest_of_path = get_token(path)
            n, rest_of_path = get_token(rest_of_path)
            while result + ',' + n in rest_of_path:
                result = result + ',' + n
                n, rest_of_path = get_token(rest_of_path)

            return result

        
        a = get_the_longest(path).strip(',')
        b = get_the_longest(path[len(a) + 1:]).strip(',')
        c = get_the_longest(path.replace(a, '').replace(b, '').strip(',')).strip(',')
        
        return [
                path.replace(a, 'A').replace(b, 'B').replace(c, 'C'),
                a,
                b,
                c
            ]


    memory = {i:v for i, v in enumerate(memory)}
    memory[0] = 2

    path = find_the_path(scaffold_map, vaccum_robot_position)
    input_for_program = [ord(c) for c in '\n'.join(split_path_to_subfunction(path) + ['n\n'])]

    for output in run_program_to_end(memory, input_for_program):
        pass

    return output


print("Solution for the second part:", solution_for_second_part(memory, scaffold_map, vaccum_robot_position))
