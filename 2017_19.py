test_map = '''     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ '''.split('\n')

def get_point(map: [str], point):
    try:
        return map[point[1] - 1][point[0] - 1]
    except Exception:
        return (' ')


assert get_point(test_map, (6, 3)) == 'A'
assert get_point(test_map, (2, 4)) == 'F'


def find_all_neighbor(map, point):
    result = []

    for point in [
        (point[0] + x, point[1] + y)
        for x in [-1, 0, 1] for y in [-1, 0, 1]
        if bool(x == 0) ^ bool(y == 0)
    ]:
        tmp = get_point(map, point)
        if tmp != ' ':
            result.append(point)

    return result


assert find_all_neighbor(test_map, (6, 2)) == [(6, 1), (6, 3)]
assert find_all_neighbor(test_map, (9, 2)) == [(9, 3), (10, 2)]
assert find_all_neighbor(test_map, (6, 6)) == [(6, 5), (7, 6)]


def walk_on_map(map: [str]):
    prev_point = (map[0].find('|') + 1, 1)
    actual_point = (map[0].find('|') + 1, 2)

    while True:        
        yield actual_point

        neighbors = find_all_neighbor(map, actual_point)
        neighbors.remove(prev_point)

        if len(neighbors) == 0:
            return
        elif len(neighbors) == 1:
            prev_point, actual_point = actual_point, neighbors[0]
        else:
            next_points = list(filter(lambda p: p[0] == prev_point[0] or p[1] == prev_point[1], neighbors))
            prev_point, actual_point = actual_point, next_points[0]


def only_letter_filter(map: [str]):
    for point in walk_on_map(map):
        character = get_point(map, point)
        if character.isalpha():
            yield character


def solution_to_first_part(map: [str]):
    return ''.join([_ for _ in only_letter_filter(map)])


assert solution_to_first_part(test_map) == 'ABCDEF'

# Input taken from https://adventofcode.com/2017/day/19/input
with open("input.txt", "r") as file:
    file_input = file.read().splitlines()

    print('Solution for the first part:', solution_to_first_part(file_input))
