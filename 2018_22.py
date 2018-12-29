from queue import PriorityQueue


X, Y, TOOL = 0, 1, 2
NOTHING, CLIMBING_GEAR, TORCH = 11, 22, 33
ROCKY, WET, NARROW = 0, 1, 2
TOOL_TABLE = {
    TORCH: [ROCKY, NARROW],
    CLIMBING_GEAR: [ROCKY, WET],
    NOTHING: [WET, NARROW]
}


class Cave:
    def __init__(self, dept, target):
        self.dept = dept
        self.target = (target[X], target[Y])
        self.cave = {}

    def get_cave_erosion_level(self, x, y):
        coord = (x, y)
        if not coord in self.cave:
            geo_index = 0

            if coord == self.target:
                geo_index = 0
            elif y == 0:
                geo_index = x * 16807
            elif x == 0:
                geo_index = y * 48271
            else:
                geo_index = self.get_cave_erosion_level(x - 1, y) * self.get_cave_erosion_level(x, y - 1)

            self.cave[coord] = (geo_index + self.dept) % 20183

        return self.cave[coord]

    def get_cave_region_type(self, point):
        return self.get_cave_erosion_level(point[X], point[Y]) % 3

    def get_neighborns(self, point):
        return [
            (point[X] + i[X], point[Y] + i[Y])
            for i in [(0, -1), (0, 1), (1, 0), (-1, 0)]
            if (point[X] + i[X]) >= 0 and (point[Y] + i[Y]) >= 0
        ]

def calculate_risk_level(cave: Cave, target):
    return sum([
        cave.get_cave_region_type((x, y))
        for y in range(0, target[Y] + 1)
        for x in range(0, target[X] + 1)
    ])


def get_neighborns(cave: Cave, point):
    other_avaible_tool = [k for k, v in TOOL_TABLE.items() if cave.get_cave_region_type((point[X], point[Y])) in v and point[TOOL] != k][0]
    
    return [(np[X], np[Y], point[TOOL])
            for np in cave.get_neighborns(point)
            if cave.get_cave_region_type(np) in TOOL_TABLE[point[TOOL]]] + [(point[X], point[Y], other_avaible_tool)]


def heuristic(_from, _to):
    return abs(_from[X] - _to[X]) + abs(_from[Y] - _to[Y])


def count_cost(cave: Cave, _from, _to):
    return 7 if _from[TOOL] != _to[TOOL] else 1


def find_the_fastest_way(cave: Cave, start_point, target):
    frontier = PriorityQueue()
    frontier.put((0, start_point))
    cost_so_far = {start_point: 0}

    while not frontier.empty():
        current = frontier.get()[1]
        if current == target:
            return cost_so_far[current]

        for next in get_neighborns(cave, current):
            new_cost = cost_so_far[current] + count_cost(cave, current, next)

            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, target)
                frontier.put((priority, next))

    return None


start_point = (0, 0, TORCH)
test_target = (10, 10, TORCH)
test_cave = Cave(510, test_target)

assert calculate_risk_level(test_cave, test_target) == 114
assert find_the_fastest_way(test_cave, start_point, test_target) == 45

# The input taken from: https://adventofcode.com/2018/day/22/input
real_target = (7, 721, TORCH)
real_cave = Cave(9171, real_target)

print("Solution for the first part:", calculate_risk_level(real_cave, real_target))
print("Solution for the second part:", find_the_fastest_way(real_cave, start_point, real_target))
