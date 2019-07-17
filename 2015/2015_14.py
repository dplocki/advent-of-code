import re


TIME_LIMIT = 2503


def load_input_file(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def parse_input(lines: [str]):
    pattern = re.compile(r'(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.')

    for line in lines:
        group = pattern.match(line)

        yield group[1], int(group[2]), int(group[3]), int(group[4])


def simulate_race(lines: [str]):


    def reindeer(speed: int, how_long: int, rest_time: int):
        while True:
            for _ in range(how_long):
                yield speed
            
            for _ in range(rest_time):
                yield 0


    reindeers = {
        name: reindeer(speed, how_long, rest_time)
        for name, speed, how_long, rest_time in parse_input(lines)
    }

    results = {}
    for _ in range(TIME_LIMIT):
        for name, reindeer in reindeers.items():
            results[name] = results.get(name, 0) + next(reindeer)

        yield results


def solution_for_first_part(lines: [str]):
    for results in simulate_race(lines):
        pass
    
    return max(results.values())


def solution_for_second_part(lines: [str]):
    points = {}

    for results in simulate_race(lines):
        maximum = max(results.values())

        for name, value in results.items():
            if value == maximum:
                points[name] = points.get(name, 0) + 1
    
    return max(points.values())


# The input is taken from: https://adventofcode.com/2015/day/14/input
print("Solution for the first part:", solution_for_first_part(load_input_file('input.14.txt')))
print("Solution for the second part:", solution_for_second_part(load_input_file('input.14.txt')))
