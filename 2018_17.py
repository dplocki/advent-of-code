import re


def parse(input: str):
    pattern = re.compile(r'^([a-z])=(\d+), [a-z]=(\d+)\.\.(\d+)$')

    for line in input:
        result = pattern.match(line)
        yield result[1] == 'x', int(result[2]), int(result[3]), int(result[4])


def input_to_map(input: str):
    result = set()

    for is_x, single, _from, _to in parse(input):
        if is_x:
            for i in range(_from, _to + 1):
                result.add((single, i))
        else:
            for i in range(_from, _to + 1):
                result.add((i, single))

    return result


def calculate_map_size(_map: set):
    return \
        (min(_map, key=lambda x: x[0])[0], max(_map, key=lambda x: x[0])[0]), \
        (min(_map, key=lambda x: x[1])[1], max(_map, key=lambda x: x[1])[1])


class SourcesSimulator:

    def __init__(self, clay_tiles):
        self.clay_tiles = clay_tiles
        (self.min_x, self.max_x), (self.min_y, self.max_y) = calculate_map_size(clay_tiles)
        self.sources = set([(500, 0)])

        self.potential_spreading_point = set()
        self.standing_watter = set()
        self.watter_tiles = set()

    def add_watter_tile(self, point):
        if point[1] >= self.min_y and point[1] <= self.max_y:
            self.watter_tiles.add(point)

    def add_source_if_can(self, point):
        if point in self.clay_tiles:
            return

        if point in self.watter_tiles:
            return

        self.sources.add(point)

    def seek_on_left(self, point):
        new_point = point
        while True:
            # checking below
            if not (new_point[0], new_point[1] + 1) in self.clay_tiles \
                and not (new_point[0], new_point[1] + 1) in self.watter_tiles:
                return None

            # checking wall on left
            if (new_point[0] - 1, new_point[1]) in self.clay_tiles:
                return new_point[0]

            new_point = (new_point[0] - 1, new_point[1])

    def seek_on_right(self, point):
        new_point = point
        while True:
            if not (new_point[0], new_point[1] + 1) in self.clay_tiles \
                and not (new_point[0], new_point[1] + 1) in self.watter_tiles:
                return None

            if (new_point[0] + 1, new_point[1]) in self.clay_tiles:
                return new_point[0]

            new_point = (new_point[0] + 1, new_point[1])

    def find_original_source(self, left, right, source):
        return [
            p
            for p in [(x, source[1] - 1) for x in range(left, right + 1)]
            if p in self.watter_tiles
        ]

    def run(self):
        while self.sources:
            source = self.sources.pop()
            if source[1] > self.max_y:  # inifity!
                continue

            self.add_watter_tile(source)
           
            tile_below = (source[0], source[1] + 1)

            if tile_below in self.clay_tiles or tile_below in self.standing_watter:
                left = self.seek_on_left(source)
                right = self.seek_on_right(source)

                if left and right:  # container
                    # flood it whole
                    for x in range(left, right + 1):
                        self.add_watter_tile((x, source[1]))
                        self.standing_watter.add((x, source[1]))

                    # move higher
                    for s in self.find_original_source(left, right, source):
                        self.sources.add(s)
                else:
                    self.add_source_if_can((source[0] - 1, source[1]))
                    self.add_source_if_can((source[0] + 1, source[1]))
            else:
                self.sources.add(tile_below)

    def visualisation(self):
        for y in range(self.min_y - 1, self.max_y + 2):
            for x in range(self.min_x - 1, self.max_x + 2):
                if (x, y) in self.clay_tiles:
                    print('#', end='')
                else:
                    if (x, y) in self.standing_watter:
                        print('~', end='')
                        continue

                    if (x, y) in self.potential_spreading_point:
                        print('x', end='')
                        continue

                    if (x, y) in self.watter_tiles:
                        print('|', end='')
                        continue

                    print('.', end='')

            print('\n', end='')


def parser(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


test_map_1 = input_to_map('''x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504'''.splitlines())
 
assert calculate_map_size(test_map_1) == ((495, 506), (1, 13))

test_simulator_1 = SourcesSimulator(test_map_1)
test_simulator_1.run()

assert len(test_simulator_1.watter_tiles) == 57

test_map_2 = input_to_map('''x=495, y=2..12
y=12, x=495..510
y=10, x=499..506
y=4, x=499..506
x=506, y=4..10
x=499, y=5..10
x=510, y=3..12
x=512, y=1..2
'''.splitlines())

test_simulator_2 = SourcesSimulator(test_map_2)
test_simulator_2.run()
assert len(test_simulator_2.watter_tiles) == 97

# The input taken from: https://adventofcode.com/2018/day/17/input 
map_input = input_to_map(parser('input.17.txt'))
first_part_simulator = SourcesSimulator(map_input)
first_part_simulator.run()

print("Solution for first part:", len(first_part_simulator.watter_tiles))
# first_part_simulator.visualisation()

assert len(test_simulator_1.standing_watter) == 29

print("Solution for second part:", len(first_part_simulator.standing_watter))
