import re


TURN_ON, TURN_OFF, TOGGLE = 11, 22, 33


def load_input_file(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def parse_input(lines: [str]):
    pattern = re.compile(r'(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)')
    for line in lines:
        groups = pattern.match(line)

        instruction = None
        if groups[1] == 'turn on':
            instruction = TURN_ON
        elif groups[1] == 'turn off':
            instruction = TURN_OFF
        elif groups[1] == 'toggle':
            instruction = TOGGLE

        yield instruction, int(groups[2]), int(groups[3]), int(groups[4]), int(groups[5])


def solution_for_the_first_part(lines_providers) -> int:
    result = set()
    instruction = {
        TURN_ON: (lambda p: result.add(p)),
        TURN_OFF: (lambda p: result.discard(p)),
        TOGGLE: (lambda p: result.remove(p) if p in result else result.add(p))
    }

    for code, start_x, start_y, end_x, end_y in parse_input(lines_providers):
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                instruction[code](1000 * y + x)

    return len(result)


def solution_for_the_second_part(lines_providers) -> int:
    result = dict()
    instruction = {
        TURN_ON: (lambda a, p: 1),
        TURN_OFF: (lambda a, p: -1 if a > 0 else 0),
        TOGGLE: (lambda a, p: 2)
    }

    for code, start_x, start_y, end_x, end_y in parse_input(lines_providers):
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                p = 1000 * y + x
                a = result.get(p, 0)
                result[p] = a + instruction[code](a, p)

    return sum(result.values())


# The input is taken from: https://adventofcode.com/2015/day/6/input
print("Solution for the first part:", solution_for_the_first_part(load_input_file('input.06.txt')))
print("Solution for the second part:", solution_for_the_second_part(load_input_file('input.06.txt')))
