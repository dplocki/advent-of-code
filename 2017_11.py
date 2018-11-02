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


def move_on_path(start, path: [str]):
    point = start
    for where in path:
        point = move(point, where)
        yield point


def count_distance_for_path(path: [str]):
    start = (0, 0, 0)
    result = start
    for point in move_on_path(start, path):
        result = point

    return distance(start, result)


def calculate_the_farst(path):
    start = (0, 0, 0)
    the_farest = 0    
    
    for point in move_on_path(start, path):
        tmp = distance(start, point)
        if tmp > the_farest:
            the_farest = tmp

    return the_farest


assert count_distance_for_path([ne,ne,ne]) == 3
assert count_distance_for_path([ne,ne,sw,sw]) == 0
assert count_distance_for_path([ne,ne,s,s]) == 2
assert count_distance_for_path([se,sw,se,sw,sw]) == 3

input = [
    # input fill up with content of https://adventofcode.com/2017/day/11/input
]

print("Solution (first part):", count_distance_for_path(input))
print("Solution (second part):", calculate_the_farst(input))
