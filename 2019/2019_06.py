CENTER_OF_MASS = 'COM'


def load_input_file(file_name: str) -> [str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def build_orbit_map(input_data: [str]) -> {}:

    def parse(lines: [str]):
        for line in lines:
            yield line.split(')')

    return { v:k for k, v in parse(input_data) }


def generate_path_from_orbit(orbits_map: {}, orbit: str) -> [str]:
    while orbit != CENTER_OF_MASS:
        orbit = orbits_map[orbit]
        yield orbit


def solution_for_first_part(orbits_map: {}) -> int:
    return sum([
            len(list(generate_path_from_orbit(orbits_map, orbit)))
            for orbit in orbits_map
        ])


test_data_for_first_part = '''COM)B
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

assert solution_for_first_part(build_orbit_map(test_data_for_first_part)) == 42

# The input is taken from: https://adventofcode.com/2019/day/6/input
orbits_map = build_orbit_map(load_input_file('input.06.txt'))
print("Solution for the first part:", solution_for_first_part(orbits_map))


def solution_for_second_part(orbits_map: {}) -> int:
    return len(
            set(generate_path_from_orbit(orbits_map, 'YOU'))
                .symmetric_difference(
                    set(generate_path_from_orbit(orbits_map, 'SAN'))
                )
        )
    

test_data_for_second_part = '''COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN'''.splitlines()

assert solution_for_second_part(build_orbit_map(test_data_for_second_part)) == 4

print("Solution for the second part:", solution_for_second_part(orbits_map))
