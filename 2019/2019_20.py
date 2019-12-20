def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: [str]):
    maze_map = {}
    positions_for_letters = {}

    for y, line in enumerate(task_input):
        for x, c in enumerate(line):
            if c in '.#':
                maze_map[x, y] = c
            elif c.isalpha():
                positions_for_letters[x, y] = c

    xs = [x for x, _ in maze_map.keys()]
    ys = [y for _, y in maze_map.keys()]
    max_x = max(xs)
    max_y = max(ys)
    min_x = min(xs)
    min_y = min(ys)

    portals = {}
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in maze_map and maze_map[x, y] == '.':
                portal_labels = [
                        positions_for_letters[f] + positions_for_letters[s]
                        for f, s in [
                            ((x + 1, y), (x + 2, y)),
                            ((x - 2, y), (x - 1, y)),
                            ((x, y + 1), (x, y + 2)),
                            ((x, y - 2), (x, y - 1))
                        ]
                        if f in positions_for_letters and s in positions_for_letters
                    ]

                if portal_labels:
                   portals[x, y] = portal_labels[0]

    aa_position = [p for p, l in portals.items() if l == 'AA'][0]
    zz_position = [p for p, l in portals.items() if l == 'ZZ'][0]

    portal_connections = {
            point: [p for p, l in portals.items() if l == label and p != point][0] # location of pair
            for point, label in portals.items()
            if not label in ['AA', 'ZZ']
        }

    return maze_map, portal_connections, aa_position, zz_position


def tradital_connections_map(maze_map: dict, portals: dict, aa_position: tuple, zz_position: tuple):

    def find_all_path_from(start_point):
        possibilites = [(start_point, 0)]
        results = {}

        while possibilites:
            position, steps = possibilites.pop(0)
            results[position] = steps

            x, y = position
            for p in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                if not p in maze_map or maze_map[p] != '.':
                    continue

                if p in results:
                    if results[p] > steps:
                        results[p] = steps
                else:
                    possibilites.append((p, steps + 1))

        return results

    return {
        portal_position: {
                point: size_of_path_to_it
                for point, size_of_path_to_it in find_all_path_from(portal_position).items()
                if (point in portals and point != portal_position) or (point == zz_position)
            }
        for portal_position in list(portals.keys()) + [aa_position]
    }


def find_the_shortest_path(portals_map: dict, portals, start_point, end_point):
    possibilites = [(start_point, 0)]
    visited = set()

    while possibilites:
        current_portal_location, path_size = possibilites.pop(0)
        visited.add(current_portal_location)

        for point, size_of_path_to_it in portals_map[current_portal_location].items():
            if point == end_point:
                return path_size + size_of_path_to_it
            elif point in visited:
                continue
            else:
                possibilites.append((portals[point], path_size + size_of_path_to_it + 1))

    return None


def solution_for_first_part(task_input):
    maze_map, portals, aa_position, zz_position = parse(task_input)
    portals_map = tradital_connections_map(maze_map, portals, aa_position, zz_position)
    return find_the_shortest_path(portals_map, portals, aa_position, zz_position)


assert solution_for_first_part('''                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               '''.splitlines()) == 58


# The input is taken from: https://adventofcode.com/2019/day/20/input
task_input = list(load_input_file('input.20.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
