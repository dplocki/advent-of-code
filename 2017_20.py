import re
from copy import deepcopy


TESTING = False
SIM_LENGHT = 1000


class Particle():

    def __init__(self, index):
        self.index = index
        self.position = None
        self.speed = None
        self.acceleration = None

    def update(self):
        for i in range(3):
            self.speed[i] += self.acceleration[i]
            self.position[i] += self.speed[i]

    def distance_from_zero(self):
        return sum([abs(self.position[i]) for i in range(3)])

    def __repr__(self):
        return f'[{self.index}] p={self.position} v={self.speed} a={self.acceleration}'


def parse_input(lines: [str]):
    pattern = re.compile(r'^p=\<(-?\d+),(-?\d+),(-?\d+)\>, v=\<(-?\d+),(-?\d+),(-?\d+)\>, a=\<(-?\d+),(-?\d+),(-?\d+)\>$')
    index = 0

    for line in lines:
        match = pattern.match(line)

        p = Particle(index)
        p.position = [int(match[s]) for s in range(1, 4)]
        p.speed = [int(match[s]) for s in range(4, 7)]
        p.acceleration = [int(match[s]) for s in range(7, 10)]
        yield p
        index += 1


def solution_for_first_part(particles: [Particle]):
    for i in range(SIM_LENGHT):
        for p in particles:
            p.update()

    return min(particles, key=lambda p: p.distance_from_zero()).index


def solution_for_second_part(particles: [Particle]) -> int:
    for _ in range(SIM_LENGHT):
        positions = {}

        for p in particles:
            p.update()

            key = tuple(p.position)
            positions[key] = positions.get(key, 0) + 1

        particles = [p for p in particles if positions[tuple(p.position)] == 1]

    return len(particles)


if TESTING:

    test_input_1 = '''p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>
p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>'''.splitlines()

    test_particles_1 = [p for p in parse_input(test_input_1)]
    assert solution_for_first_part(test_particles_1) == 0

    test_input_2 = '''p=<-6,0,0>, v=<3,0,0>, a=<0,0,0>
p=<-4,0,0>, v=<2,0,0>, a=<0,0,0>
p=<-2,0,0>, v=<1,0,0>, a=<0,0,0>
p=<3,0,0>, v=<-1,0,0>, a=<0,0,0>'''.splitlines()

    test_particles_2 = [p for p in parse_input(test_input_2)]
    assert solution_for_second_part(test_particles_2) == 1

else:

    def file_to_input_list(file_name):
        with open(file_name) as file:
            for line in file:
                yield line.strip()

    # The input taken from: https://adventofcode.com/2017/day/20/input
    task_particles = [p for p in parse_input(file_to_input_list('input.20.txt'))]
    print("Solution for the first part:", solution_for_first_part(deepcopy(task_particles)))
    print("Solution for the second part:", solution_for_second_part(task_particles))
