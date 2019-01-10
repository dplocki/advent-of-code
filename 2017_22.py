UP, DOWN, RIGTH, LEFT = 11, 22, 33, 44


def file_to_input_list(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def parse_input(lines: [str]):
    start_x = 0
    x, y = 0, 0
    size = None

    for line in lines:
        if not size:
            size = len(line)
            start_x = 0 - size // 2
            y = 0 - size // 2

        x = start_x
        for char in line:
            if char == '#':
                yield (x, y)

            x += 1
        y += 1


def node_generator(initial_input: [str]):
    nodes = set()
    for p in parse_input(initial_input):
        nodes.add(p)

    current_position = (0, 0)
    oriented = UP
    result = 0

    while True:
        if current_position in nodes:
            # right
            if oriented == UP:
                oriented = RIGTH
            elif oriented == DOWN:
                oriented = LEFT        
            elif oriented == RIGTH:
                oriented = DOWN
            elif oriented == LEFT:
                oriented = UP
        else:
            # left
            if oriented == UP:
                oriented = LEFT
            elif oriented == DOWN:
                oriented = RIGTH        
            elif oriented == RIGTH:
                oriented = UP
            elif oriented == LEFT:
                oriented = DOWN

        if current_position in nodes:
            nodes.remove(current_position)
        else:
            nodes.add(current_position)
            result += 1

        if oriented == UP:
            current_position = (current_position[0], current_position[1] - 1)
        elif oriented == DOWN:
            current_position = (current_position[0], current_position[1] + 1)
        elif oriented == RIGTH:
            current_position = (current_position[0] + 1, current_position[1])
        elif oriented == LEFT:
            current_position = (current_position[0] - 1, current_position[1])

        yield result


def run_generator_n_times(initial_input: [str], n: int):
    test_generator = node_generator(initial_input)
    for result, i in zip(test_generator, range(n)):
        pass

    return result


test_input = '''..#
#..
...'''.splitlines()

assert run_generator_n_times(test_input, 70) == 41
assert run_generator_n_times(test_input, 10000) == 5587

# The input is taken from https://adventofcode.com/2017/day/22/input
print("The solution for the first part:", run_generator_n_times(file_to_input_list('input.22.txt'), 10000))
