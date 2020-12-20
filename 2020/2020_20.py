import re
from collections import Counter
from functools import reduce 
from operator import mul


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def parse(task_input: [str]):

    def parse_tile(tile):
        for y, line in enumerate(tile):
            yield from ((x, y) for x, c in enumerate(line) if c == '#')


    tile_title_pattern = re.compile('Tile (\d+):')

    for raw_tile in task_input.split('\n\n'):
        lines = raw_tile.splitlines()
        title_id = int(tile_title_pattern.match(lines[0])[1])

        yield title_id, set(parse_tile(lines[1:]))


def edge_to_number(tile, point):
    return int(''.join(['1' if p in tile else '0' for p in point]), 2)


def all_possible_edges(tile):
    n = edge_to_number(tile, ((i, 0) for i in range(10)))
    w = edge_to_number(tile, ((0, i) for i in range(10)))
    e = edge_to_number(tile, ((9, i) for i in range(10)))
    s = edge_to_number(tile, ((i, 9) for i in range(10)))

    rn = edge_to_number(tile, ((9 - i, 0) for i in range(10)))
    rw = edge_to_number(tile, ((0, 9 - i) for i in range(10)))
    re = edge_to_number(tile, ((9, 9 - i) for i in range(10)))
    rs = edge_to_number(tile, ((9 - i, 9) for i in range(10)))

    return [ n, w, e, s, rn, rw, re, rs ]


def solution_for_first_part(task_input):

    def is_tile_a_corner(edges, corners_edges):
        return sum(1 for edge in edges if edge in corners_edges) == 4


    tiles = {tile_id: all_possible_edges(tile) for tile_id, tile in parse(task_input)}
    count_edges = Counter(edge for edges in tiles.values() for edge in edges)
    corners_edges = [edge for edge, how_many_appear in count_edges.items() if how_many_appear == 1]

    return reduce(mul, (tile_id for tile_id, tile in tiles.items() if is_tile_a_corner(tile, corners_edges)))


example_input = '''Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...'''

assert solution_for_first_part(example_input) == 20899048083289

# The input is taken from: https://adventofcode.com/2020/day/20/input
task_input = load_input_file('input.20.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
