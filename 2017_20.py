import re


TESTING = False


class Particle():

    def __init__(self, index):
        self.index = index
        self.position = None
        self.speed = None
        self.acceleration = None

    def update(self):
        for i in range(3):
            self.position[i] += self.speed[i]
            self.speed[i] += self.acceleration[i]

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
    for i in range(1000):
        for p in particles:
            p.update()

    return min(particles, key=lambda p: p.distance_from_zero()).index


if TESTING:

    test_input = '''p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>
p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>'''.splitlines()

    particles = [p for p in parse_input(test_input)]
    assert solution_for_first_part(particles) == 0

else:

    def file_to_input_list(file_name):
        with open(file_name) as file:
            for line in file:
                yield line.strip()

    # The input taken from: https://adventofcode.com/2017/day/20/input
    task_particles = [p for p in parse_input(file_to_input_list('input.20.txt'))]
    print("Solution for the first part:", solution_for_first_part(task_particles))
