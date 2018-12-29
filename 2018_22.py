def create_cave(max_x = 10, max_y = 10, dept = 510):
    cave = {}
    for y in range(0, max_y + 1):
        for x in range(0, max_x + 1):
            geo_index = 0
            if (x, y) == (0, 0) or (x, y) == (max_x, max_y):
                geo_index = 0
            elif y == 0:
                geo_index = x * 16807
            elif x == 0:
                geo_index = y * 48271
            else:
                geo_index = cave[(x - 1, y)] * cave[(x, y - 1)]

            cave[(x, y)] = (geo_index + dept) % 20183

    return cave


def calculate_risk_level(cave: {}):
    return sum([p % 3 for p in cave.values()])


assert calculate_risk_level(create_cave(10, 10, 510)) == 114

# The input taken from: https://adventofcode.com/2018/day/22/input
print("Solution for the first part:", calculate_risk_level(create_cave(7, 721, 9171)))
