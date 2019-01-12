import re
import sys


test_input = '''position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>'''.split('\n')


def parser(lines: [str]):
    pattern = re.compile(r'^position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>$')

    for line in lines:
        result = pattern.match(line)
        yield (int(result[1]), int(result[2])), (int(result[3]), int(result[4]))
 

def get_points_and_velocities(input: []):
    points = []
    velocity = []
    for p, v in input:
        points.append(p)
        velocity.append(v)
    
    return points, velocity


def second_passing(points, velocity):
    return [(p[0] + v[0], p[1] + v[1]) for p, v in zip(points, velocity)]


def calculate_size_of_field(points):
    min_x = min(points, key=lambda p: p[0])[0]
    max_x = max(points, key=lambda p: p[0])[0]

    min_y = min(points, key=lambda p: p[1])[1]
    max_y = max(points, key=lambda p: p[1])[1]

    x_size = abs(max_x - min_x) + 1
    y_size = abs(max_y - min_y) + 1

    return (min_x, min_y), (x_size, y_size)


def ligths_to_string(points):
    start_point, size = calculate_size_of_field(points)

    result = [['.'] * size[0] for _ in range(size[1])]

    for p in points:
        x = p[0] - start_point[0]
        y = p[1] - start_point[1]

        result[y][x] = '#'

    return '\n'.join([''.join(result[y]) for y in range(size[1])])


test_result_points, _ = get_points_and_velocities(parser(test_input))
assert ligths_to_string(test_result_points) == '''........#.............
................#.....
.........#.#..#.......
......................
#..........#.#.......#
...............#......
....#.................
..#.#....#............
.......#..............
......#...............
...#...#.#...#........
....#..#..#.........#.
.......#..............
...........#..#.......
#...........#.........
...#.......#..........'''


def read_line_from_file(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def calculate_field(points):
    _, size = calculate_size_of_field(points)
    field = size[0] * size[1]

    return field


def score_generator(input):
    points, vectors = get_points_and_velocities(input)
    prev_field = sys.maxsize
    prev_points = None
    seconds = 0

    while True:
        field = calculate_field(points)
        if field > prev_field:
            return prev_points, seconds - 1

        prev_field = field
        prev_points = points

        points = second_passing(points, vectors)
        seconds += 1


_, test_time_result = score_generator(parser(test_input))
assert test_time_result == 3

# Taken from https://adventofcode.com/2018/day/10/input
points, seconds = score_generator(parser(read_line_from_file('input.txt')))
print("Solution to first part:")
print(ligths_to_string(points))
print("Solution to second part:", seconds)
