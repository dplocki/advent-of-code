import re


X, Y, Z, R = 0, 1, 2, 3


def parse_input(lines: [str]):
    pattern = re.compile(r'^pos=\<(-?\d+),(-?\d+),(-?\d+)\>, r=(\d+)$')

    for line in lines:
        match = pattern.match(line)
        yield tuple([int(match[i]) for i in range(1, 5)])


def distance(p1, p2):
    return sum([abs(p2[i] - p1[i]) for i in range(3)])


def read_file(file_name: str):
    with open(file_name) as f:
        for line in f:
            yield line


def calc_how_many_bots_are_in_radious_of_strongest(nanobots):
    strongest = max(nanobots, key=lambda n: n[R])
    return len([
        n for n in nanobots
        if distance(n, strongest) <= strongest[R]
    ])


test_input = '''pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1'''.splitlines()

test_nanobots = [_ for _ in parse_input(test_input)]
assert calc_how_many_bots_are_in_radious_of_strongest(test_nanobots) == 7

# The input taken from: https://adventofcode.com/2018/day/23/input
nanobots = [_ for _ in parse_input(read_file('input.23.txt'))]
print("Solution for the first part:", calc_how_many_bots_are_in_radious_of_strongest(nanobots))
