CENTER_OF_MASS = 'COM'


def load_input_file(file_name: str) -> [str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def build_orbit_map(input_data: [str]) -> {}:

    def parse(lines: [str]):
        for line in lines:
            yield line.split(')')

    return { v:k for k, v in parse(input_data) }


def solution_for_first_part(orbits_map: {}) -> int:
    result = 0
    for orbit in orbits_map:
        while True:
            orbit = orbits_map[orbit]
            result += 1
            if orbit == CENTER_OF_MASS:
                break

    return result


test_data = '''COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L'''.splitlines()

assert solution_for_first_part(build_orbit_map(test_data)) == 42

# The input is taken from: https://adventofcode.com/2019/day/6/input
orbits_map = build_orbit_map(load_input_file('input.06.txt'))
print("Solution for the first part:", solution_for_first_part(orbits_map))
