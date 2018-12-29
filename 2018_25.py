import itertools


def parse_input(lines: [str]):
    for line in lines:
        yield tuple([int(t) for t in line.split(',')])


def distance(p1, p2):
    return sum([abs(p2[i] - p1[i]) for i in range(4)])


def read_file(file_name):
    with open(file_name) as f:
        for line in f:
            yield line


def assign_constelations(coordinates):

    def build_graph(coordinates: []):
        graph = { c:set() for c in coordinates }
        for p1, p2 in itertools.combinations(coordinates, 2):
            if p1 != p2 and distance(p1, p2) <= 3:
                graph[p1].add(p2)
                graph[p2].add(p1)

        return graph

    def find_all(graph, p, was):
        was.add(p)
        for s in graph[p]:
            if s in was:
                continue

            yield s
            was.add(s)
            for x in find_all(graph, s, was):
                yield x

    index = 0
    constelations = {}
    graph = build_graph(coordinates)

    for c in coordinates:
        if c in constelations:
            continue

        constelations[c] = index
        for x in find_all(graph, c, set()):
            constelations[x] = index
        
        index += 1

    return constelations


def calculate_first_part(input):
    coordinates = [coordinate for coordinate in parse_input(input)]
    constelations = assign_constelations(coordinates)

    return len(set(constelations.values()))


test_input_1 = '''0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0'''.splitlines()

assert calculate_first_part(test_input_1) == 2

test_input_2 = '''1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2'''.splitlines()

assert calculate_first_part(test_input_2) == 3

test_input_3 = '''1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2'''.splitlines()

assert calculate_first_part(test_input_3) == 8

# The input taken from: https://adventofcode.com/2018/day/25/input
real_input = read_file('input.25.txt')

print("Solution for the first part:", calculate_first_part(real_input))
