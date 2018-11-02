n = 'n'
s = 's'
ne = 'ne'
se = 'se'
nw = 'nw'
sw = 'sw'


def move(point, direction):
    if direction == n:
        return (point[0] + 1, point[1], point[2] - 1)
    elif direction == s:
        return (point[0] - 1, point[1], point[2] + 1)
    elif direction == ne:
        return (point[0] + 1, point[1] - 1, point[2])
    elif direction == se:
        return (point[0], point[1] - 1, point[2] + 1)
    elif direction == nw:
        return (point[0], point[1] + 1, point[2] - 1)
    elif direction == sw:
        return (point[0] - 1, point[1] + 1, point[2])


def distance(begin, end):
    return (abs(begin[0] - end[0]) + abs(begin[1] - end[1]) + abs(begin[2] - end[2])) / 2


def count_distance_for_path(path):
    start = (0, 0, 0)
    point = start
    for where in path:
        point = move(point, where)

    return distance(start, point)


assert count_distance_for_path([ne,ne,ne]) == 3
assert count_distance_for_path([ne,ne,sw,sw]) == 0
assert count_distance_for_path([ne,ne,s,s]) == 2
assert count_distance_for_path([se,sw,se,sw,sw]) == 3

input = [
    # input fill up with content of https://adventofcode.com/2017/day/11/input
]
print("Solution (first part):", count_distance_for_path(input))
