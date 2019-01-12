import re
import heapq
import itertools


TESTING = False
X, Y, Z, RADIOUS = 0, 1, 2, 3


def parse_input(lines: [str]):
    pattern = re.compile(r'^pos=\<(-?\d+),(-?\d+),(-?\d+)\>, r=(\d+)$')

    for line in lines:
        match = pattern.match(line)
        yield tuple([int(match[i]) for i in range(1, 5)])


def distance(p1, p2):
    return sum([abs(p2[i] - p1[i]) for i in range(3)])


def calc_how_many_bots_are_in_radious_of_strongest(nanobots):
    strongest = max(nanobots, key=lambda n: n[RADIOUS])
    return len([
        n for n in nanobots
        if distance(n, strongest) <= strongest[RADIOUS]
    ])


class Box():
    def __init__(self, bmin, size):
        self._bmin = bmin
        self.size = size

    def bmin(self):
        return self._bmin

    def bmax(self):
        return [self._bmin[i] + self.size for i in range(3)]

    def __repr__(self):
        return f'{self._bmin} s:{self.size}'

    def __lt__(self, other):
        # I don't need to sort by box
        return None


def find_the_most_in_range_coordinates(nanobots: [tuple]) -> tuple:


        def distance_in_dimention(d, low, high):
            if d < low: return low - d
            if d > high: return d - high
            return 0


        def distance_from_box(box: Box, bot) -> bool:
            return sum([
                distance_in_dimention(bot[i], box._bmin[i], box._bmin[i] + box.size -1)
                for i in range(3)]) <= bot[RADIOUS]


        def how_much_bots(nanobots, box: Box) -> int:
            return len([bot for bot in nanobots if distance_from_box(box, bot)])


        def split_box_on_eight(box: Box):


            def spliting_point_for_box(bmin, bmax):
                return tuple([
                    bmin[i] + abs(bmax[i] - bmin[i]) // 2
                    for i in range(3)
                ])

            size = box.size // 2
            p = [box.bmin(), spliting_point_for_box(box.bmin(), box.bmax())]
            for ix, iy, iz in itertools.product([0, 1], repeat=3):
                yield Box((p[ix][0], p[iy][1], p[iz][2]), size)


        def the_lowest_2_power_for(x):
            return 1<<(x-1).bit_length()


        def distance_from_center(box: Box):
            return sum([abs(box._bmin[i]) for i in range(3)])


        mins = [min(nanobots, key=lambda t: t[i])[i] for i in range(3)]
        length = max([abs(max(nanobots, key=lambda t: t[i])[i] - mins[i]) for i in range(3)])
        initial_box_size = the_lowest_2_power_for(length)

        box = Box(tuple([mins[i] for i in range(3)]), initial_box_size)
        queue = [(0, initial_box_size, len(nanobots), box)]
        heapq.heapify(queue)
        
        while queue:
            _, distance, size, box = heapq.heappop(queue)
            if size == 1:
                return distance

            boxes = {
                (small_box): how_much_bots(nanobots, small_box)
                for small_box in split_box_on_eight(box)
            }

            for box, bots_number in boxes.items():
                heapq.heappush(queue, (-bots_number, distance_from_center(box), box.size, box))


if TESTING:

    test_input = '''pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1'''

    test_nanobots = [_ for _ in parse_input(test_input.splitlines())]
    assert calc_how_many_bots_are_in_radious_of_strongest(test_nanobots) == 7

    test_input_2 = '''pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5'''

    test_nanobots_2 = [_ for _ in parse_input(test_input_2.splitlines())]
    result = find_the_most_in_range_coordinates(test_nanobots_2)
    assert result == 36

else:

    def read_file(file_name: str):
        with open(file_name) as f:
            for line in f:
                yield line

    # The input taken from: https://adventofcode.com/2018/day/23/input
    real_nanobots = [_ for _ in parse_input(read_file('input.23.txt'))]

    print("Solution for the first part:", calc_how_many_bots_are_in_radious_of_strongest(real_nanobots))
    print("Solution for the second part:", find_the_most_in_range_coordinates(real_nanobots))
