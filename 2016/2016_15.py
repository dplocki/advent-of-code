import re

def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(lines: [str]):

    def pre_parse(lines):
        pattern = re.compile(r'Disc #(\d) has (\d+) positions; at time=0, it is at position (\d+)\.')

        for line in lines:
            group = pattern.match(line)
            yield int(group[1]), int(group[2]), int(group[3])

    return {index: (size, start_position) for index, size, start_position in pre_parse(lines)}


def simulation(discs: {}, start_time: int) -> bool:
    fall = 1

    while fall <= len(discs):
        size, start_position = discs[fall]

        if (start_position + start_time + fall) % size != 0:
            return False

        fall += 1

    return True


def solution_for_first_part(disc):
    time = 0
    while True:
        if simulation(discs, time):
            return time

        time += 1


test_input = parse('''Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.'''.splitlines())

assert simulation(test_input, 0) == False
assert simulation(test_input, 5) == True

# The input is taken from: https://adventofcode.com/2016/day/15/input
discs = parse(load_input_file('input.15.txt'))

print("Solution for the first part:", solution_for_first_part(discs))


def solution_for_second_part(disc):
    discs[len(discs) + 1] = (11, 0)
    return solution_for_first_part(discs)


print("Solution for the second part:", solution_for_second_part(discs))
