RECT_COMMAND = 0
ROW_COMMAND = 1
COLUMN_COMMAND = 2


def load_input_file(file_name: str):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def screen_update(screen_tall: int, screen_wide: int, input_lines: [str]):


    def parse_input_line(line):
        if 'rect' in line:
            tmp = line.split(' ')[1].split('x')
            return RECT_COMMAND, int(tmp[0]), int(tmp[1])

        tmp = line.split('=')[1].split(' by ')
        return ROW_COMMAND if 'row' in line else COLUMN_COMMAND, int(tmp[0]), int(tmp[1])


    def flat_coordinates(x, y):
        return y * screen_wide + x


    screen = set()
    for line in input_lines:
        instraction, parameter_a, parameter_b = parse_input_line(line)

        if instraction == RECT_COMMAND:
            for x in range(parameter_a):
                for y in range(parameter_b):
                    screen.add(flat_coordinates(x, y))

        elif instraction == COLUMN_COMMAND:
            base = [flat_coordinates(parameter_a, i) in screen for i in range(screen_tall)]

            for i in range(screen_tall):
                if base[(i - parameter_b) % screen_tall]:
                    screen.add(flat_coordinates(parameter_a, i))
                else:
                    screen.discard(flat_coordinates(parameter_a, i))

        elif instraction == ROW_COMMAND:
            base = [flat_coordinates(i, parameter_a) in screen for i in range(screen_wide)]

            for i in range(screen_wide):
                if base[(i - parameter_b) % screen_wide]:
                    screen.add(flat_coordinates(i, parameter_a))
                else:
                    screen.discard(flat_coordinates(i, parameter_a))

        yield screen


def solution_for_first_part(input_lines: [str]) -> int:
    SCREEN_TALL = 6
    SCREEN_WIDE = 50

    for screen in screen_update(SCREEN_TALL, SCREEN_WIDE, input_lines):
        pass

    return len(screen)

test_screen_tall = 3
test_screen_wide = 7
test_input = [
    'rect 3x2',
    'rotate column x=1 by 1',
    'rotate row y=0 by 4',
    'rotate column x=1 by 1'
]

# The input is taken from: https://adventofcode.com/2016/day/8/input
input_lines = load_input_file('input.08.txt')
print("Solution for the first part:", solution_for_first_part(input_lines))
