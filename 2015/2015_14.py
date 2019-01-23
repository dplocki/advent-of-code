import re


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
    for i in range(2503):
        for name, reindeer in reindeers.items():
            results[name] = results.get(name, 0) + next(reindeer)

    return results


# The solution is taken from: https://adventofcode.com/2015/day/14/input
print("Solution for the first part:", max(simulate_race(load_input_file('input.14.txt')).values()))
