import itertools
import math


AXIES_NUMBER = 3


def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(lines: [str]):
    for line in lines:
        line = line[1:-1]
        tokens = line.split(', ')

        yield [int(token[2:]) for token in tokens]


def all_axies():
    return range(AXIES_NUMBER)


def velocity_change_for_ax(position_a, velocity_a, position_b, velocity_b):
    if position_a > position_b:
        return velocity_a - 1, velocity_b + 1
    elif position_a < position_b:
        return velocity_a + 1, velocity_b - 1

    return velocity_a, velocity_b


def step_generator(positions, velocities):
    while True:
        for a, b in itertools.combinations(positions.keys(), 2):
            for ax in all_axies():
                velocities[a][ax], velocities[b][ax] = velocity_change_for_ax(positions[a][ax], velocities[a][ax], positions[b][ax], velocities[b][ax])

        for moon in positions.keys():
            positions[moon] = [positions[moon][ax] + velocities[moon][ax] for ax in all_axies()]

        yield positions, velocities


def get_total_energy_of_system_after_steps(positions, velocities, steps):

    def get_total_energy_of_system(positions, velocities):
        moons = positions.keys()
        potentials = [sum([abs(positions[moon][ax]) for ax in all_axies()]) for moon in moons]
        kinetics = [sum([abs(velocities[moon][ax]) for ax in all_axies()]) for moon in moons]

        return sum([potentials[moon] * kinetics[moon] for moon in moons])

    for _, result in zip(range(steps), step_generator(positions, velocities)):
        positions, velocities = result

    return get_total_energy_of_system(positions, velocities)


def get_initial_positions_and_velicities(moons_positions_list):
    positions = {moon:position for moon, position in enumerate(moons_positions_list)}
    velocities = {moon:[0, 0, 0] for moon, _ in enumerate(moons_positions_list)}

    return positions, velocities


def solution_for_first_task(moons_positions_list):
    positions, velocities = get_initial_positions_and_velicities(moons_positions_list)

    return get_total_energy_of_system_after_steps(positions, velocities, 1000)


# The input is taken from: https://adventofcode.com/2019/day/12/input
moons_positions_list = list(parse(load_input_file('input.12.txt')))
print("Solution for the first part:", solution_for_first_task(moons_positions_list))


def solution_for_second_task(moons_positions_list):

    def cycles_length_finder(positions, velocities):

        def hash_state_on_ax(ax, positions, velocities):
            return tuple([(positions[moon][ax], velocities[moon][ax]) for moon in positions.keys()])

        cycle_step_per_ax = {ax:None for ax in all_axies()}
        positions_per_ax = {ax:set([hash_state_on_ax(ax, positions, velocities)]) for ax in all_axies()}

        step = 1
        for positions, velocities in step_generator(positions, velocities):
            for ax in all_axies():
                tmp = hash_state_on_ax(ax, positions, velocities)
                if tmp in positions_per_ax[ax]:
                    cycle_step_per_ax[ax] = cycle_step_per_ax[ax] or step

                positions_per_ax[ax].add(tmp)
                if not None in cycle_step_per_ax.values():
                    return cycle_step_per_ax.values()

            step += 1

    def lcm(x, y):
        return (x*y) // math.gcd(x,y)

    positions, velocities = get_initial_positions_and_velicities(moons_positions_list)
    results = cycles_length_finder(positions, velocities)
    prev = 1
    for result in results:
        prev = lcm(prev, result)

    return prev
    

assert solution_for_second_task(list(parse('''<x= -1, y=  0, z=  2>
<x=  2, y=-10, z= -7>
<x=  4, y= -8, z=  8>
<x=  3, y=  5, z= -1>'''.splitlines()))) == 2772

assert solution_for_second_task(list(parse('''<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>'''.splitlines()))) == 4686774924

print("Solution for the second part:", solution_for_second_task(moons_positions_list))
