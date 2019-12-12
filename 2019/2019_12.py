import itertools


def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(lines: [str]):
    for line in lines:
        line = line[1:-1]
        tokens = line.split(', ')

        yield [int(t[2:]) for t in tokens]


def step_generator(positions, velocities):
    while True:
        for a, b in itertools.combinations(positions.keys(), 2):
            for ax in range(3):
                if positions[a][ax] > positions[b][ax]:
                    velocities[a][ax] -= 1
                    velocities[b][ax] += 1
                elif positions[a][ax] < positions[b][ax]:
                    velocities[a][ax] += 1
                    velocities[b][ax] -= 1

        for p in positions.keys():
            positions[p] = [positions[p][0] + velocities[p][0], positions[p][1] + velocities[p][1], positions[p][2] + velocities[p][2]]

        yield positions, velocities


def get_total_energy_of_system_after_steps(positions, velocities, steps):

    def get_total_energy_of_system(positions, velocities):
        potentials = [abs(positions[p][0]) + abs(positions[p][1]) + abs(positions[p][2]) for p in positions.keys()]
        kinetics = [abs(velocities[p][0]) + abs(velocities[p][1]) + abs(velocities[p][2]) for p in positions.keys()]

        return sum([potentials[p] * kinetics[p] for p in positions.keys()])

    for _, result in zip(range(steps), step_generator(positions, velocities)):
        positions = result[0]
        velocities = result[1]

    return get_total_energy_of_system(positions, velocities)


def solution_for_first_task(moons_positions_list):
    positions = { p:k for p, k in enumerate(moons_positions_list) }
    velocities = { p:[0, 0, 0] for p, _ in enumerate(moons_positions_list)}

    return get_total_energy_of_system_after_steps(positions, velocities, 1000)


# The input is taken from: https://adventofcode.com/2019/day/12/input
moons_positions_list = list(parse(load_input_file('input.12.txt')))
print("Solution for the first part:", solution_for_first_task(moons_positions_list))
