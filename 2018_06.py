import sys
from collections import defaultdict
import string


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, point) -> int:
        return abs(self.x - point.x) + abs(self.y - point.y)

    def __eq__(self, other):
        if not other:
            return False

        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"(x: {self.x}, y: {self.y})"

    def __repr__(self):
        return self.__str__()

class Coordinate(Point):
    def __init__(self, id, x, y):
        Point.__init__(self, x, y)
        self.id = id

def parse_lines(lines: []) -> [Coordinate]:
    id = 1
    for line in lines:
        tmp = line.split(', ')
        yield Coordinate(id, int(tmp[0]), int(tmp[1]))
        id += 1


def calculate_size_of_finit_part(coordinates: [Coordinate]) -> (Point, Point):
    start_x = min(coordinates, key=lambda p: p.x).x
    start_y = min(coordinates, key=lambda p: p.y).y

    end_x = max(coordinates, key=lambda p: p.x).x
    end_y = max(coordinates, key=lambda p: p.y).y

    return Point(start_x, start_y), Point(end_x, end_y)


def find_closest_single_point_from(point: Point, coordinates: [Point]):
    closest_point = None
    min_distance = sys.maxsize
    is_single = True

    for coordinate in coordinates:
        distance = point.distance(coordinate)
        if distance == min_distance:
            is_single = False
        elif distance < min_distance:
            closest_point = coordinate
            min_distance = distance
            is_single = True

    return closest_point if is_single else None


def find_all_inifity_points(coordinates: [Point], left_top: Point, right_bottom: Point):
    result = set()
    
    points = [find_closest_single_point_from(Point(ix, left_top.y), coordinates) for ix in range(left_top.x, right_bottom.x)]
    result.update([p.id for p in points if p])

    points = [find_closest_single_point_from(Point(ix, right_bottom.y), coordinates) for ix in range(left_top.x, right_bottom.x)]
    result.update([p.id for p in points if p])

    points = [find_closest_single_point_from(Point(left_top.x, iy), coordinates) for iy in range(left_top.y, right_bottom.y)]
    result.update([p.id for p in points if p])

    points = [find_closest_single_point_from(Point(right_bottom.x, iy), coordinates) for iy in range(left_top.y, right_bottom.y)]
    result.update([p.id for p in points if p])

    return result


def visualization(coordinates: [Coordinate], left_top: Point, right_bottom: Point):
    result = ''
    for y in range(left_top.y -1, right_bottom.y +2):
        for x in range(left_top.x -1, right_bottom.x+ 2):
            point = Point(x, y)
            coordinate = find_closest_single_point_from(point, coordinates)
            if point == coordinate:
                result += string.ascii_uppercase[coordinate.id - 1]
            else:
                result += string.ascii_lowercase[coordinate.id - 1] if coordinate else '.'

        result += '\n'

    return result


def calculate_closest_distance_hashtable(coordinates: [Coordinate], rejected: set, left_top: Point, right_bottom: Point):
    all_points = [Point(x, y) for x in range(left_top.x, right_bottom.x) for y in range(left_top.y, right_bottom.y)]
    result_table = defaultdict(lambda: 0)

    for point in all_points:
        coordinate = find_closest_single_point_from(point, coordinates)
        if coordinate and not coordinate.id in rejected:
            result_table[coordinate.id] += 1

    return result_table
    

test_input = ['1, 1', '1, 6', '8, 3', '3, 4', '5, 5', '8, 9']
parsed_test_result = [_ for _ in parse_lines(test_input)]
test_border_points = calculate_size_of_finit_part(parsed_test_result)

assert test_border_points == (Point(1,1), Point(8,9))

assert Point(0, 0).distance(Point(1, 1)) == 2
assert Point(1, 1).distance(Point(3, 2)) == 3

assert find_closest_single_point_from(Point(0, 0), parsed_test_result) == parsed_test_result[0]
assert find_closest_single_point_from(Point(5, 1), parsed_test_result) == None
assert find_closest_single_point_from(Point(1, 1), parsed_test_result) == parsed_test_result[0] # A
assert find_closest_single_point_from(Point(1, 6), parsed_test_result) == parsed_test_result[1] # B
assert find_closest_single_point_from(Point(8, 3), parsed_test_result) == parsed_test_result[2] # C
assert find_closest_single_point_from(Point(3, 4), parsed_test_result) == parsed_test_result[3] # D
assert find_closest_single_point_from(Point(5, 5), parsed_test_result) == parsed_test_result[4] # E
assert find_closest_single_point_from(Point(8, 9), parsed_test_result) == parsed_test_result[5] # F

test_rejected_result = find_all_inifity_points(parsed_test_result, *test_border_points)

assert test_rejected_result == set([1, 2, 3, 6]) # A B C F

test_result_distance_table = calculate_closest_distance_hashtable(parsed_test_result, test_rejected_result, *test_border_points)

assert len(test_result_distance_table.keys()) == 2
assert test_result_distance_table[4] == 9 # D
assert test_result_distance_table[5] == 17 # E


def calculate_solution_for_first_part(input: [str]):
    coordinates = [_ for _ in parse_lines(input)]
    border_points = calculate_size_of_finit_part(coordinates)
    infinit_coordinates = find_all_inifity_points(coordinates, *border_points)

    #print(visualization(coordinates, *border_points))

    result_distance_table = calculate_closest_distance_hashtable(coordinates, infinit_coordinates, *border_points)

    return max(result_distance_table.values())


assert calculate_solution_for_first_part(test_input) == 17


def load_file(file_name):
    been = set()
    with open(file_name) as file:
        for line in file:
            if not line in been:
                been.add(line)
                yield line.strip()


# The input taken from: https://adventofcode.com/2018/day/6/input
print('Solution for first part:', calculate_solution_for_first_part(load_file('input.txt')))
