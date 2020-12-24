import re
from itertools import permutations
from collections import Counter
from functools import reduce
from operator import mul
from math import floor


# Clockwise
NORTH, EAST, SOUTH, WEST = range(4)
FIRST_TILE = (0, 0)
PICTURE_SIZE_WITH_BORDERS = 8


def parse_image(tile):
    for y, line in enumerate(tile):
        yield from ((x, y) for x, c in enumerate(line) if c == '#')


def parse(task_input: [str]):
    tile_title_pattern = re.compile('Tile (\d+):')

    for raw_tile in task_input.split('\n\n'):
        lines = raw_tile.splitlines()
        title_id = int(tile_title_pattern.match(lines[0])[1])

        yield title_id, set(parse_image(lines[1:]))


class Tile():

    def __init__(self, _id, body):
        self.id = _id
        self.body = body
        self.transformations = ''
        self.all_possible_edges = all_possible_edges(self.body)

        n, e, s, w, rn, re, rs, rw = self.all_possible_edges
        self.current_edges = (n, e, s, w)
        self.rotate_matrix = {v:l for v,l in bulid_edges_after_all_transformations(*self.all_possible_edges)}

    def orient_on_north_and_west(self, north, west):
        for pointer_path, transformations in self.rotate_matrix.items():
            if pointer_path[NORTH] == north and pointer_path[WEST] == west:
                self.current_edges = pointer_path
                self.transformations = transformations
                return True

        return False

    def get_north_if_west(self, west):
        yield from (n for n, e, s, w in self.rotate_matrix.keys() if w == west)

    def get_west_if_north(self, north):
        yield from (w for n, e, s, w in self.rotate_matrix.keys() if n == north)

    def cut_edges(self):
        return set(
            (x - 1, y - 1)
            for x in range(10)
            for y in range(10)
            if 0 < x < 9 and 0 < y < 9 and (x, y) in self.body)

    def __repr__(self):
        return f'ID: {self.id} TRANSFORMATION: "{self.transform}"'


def bulid_edges_after_all_transformations(n, e, s, w, rn, re, rs, rw):
    reverse = {
        n: rn,
        rn: n,
        w: rw,
        rw: w,
        e: re,
        re: e,
        s: rs,
        rs: s
    }

    starting = {
        (rs, rw, rn, re): 'vh',
        (s, re, n, rw): 'h',
        (rn, w, rs, e): 'v',
        (n, e, s, w): ''
    }

    rotate = lambda n, e, s, w: (reverse[w], n, reverse[e], s)
    for start, label in starting.items():
        for angle in range(4):
            yield start, label + "r" * angle
            start = rotate(*start)


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def edge_to_number(tile, point):
    return int(''.join(['1' if p in tile else '0' for p in point]), 2)


def all_possible_edges(tile):
    n = edge_to_number(tile, ((i, 0) for i in range(10)))
    e = edge_to_number(tile, ((9, i) for i in range(10)))
    s = edge_to_number(tile, ((i, 9) for i in range(10)))
    w = edge_to_number(tile, ((0, i) for i in range(10)))

    rn = edge_to_number(tile, ((9 - i, 0) for i in range(10)))
    re = edge_to_number(tile, ((9, 9 - i) for i in range(10)))
    rs = edge_to_number(tile, ((9 - i, 9) for i in range(10)))
    rw = edge_to_number(tile, ((0, 9 - i) for i in range(10)))

    return (n, e, s, w, rn, re, rs, rw)


def is_tile_a_corner(corners_edges: set):

    def internal(edges: list) -> bool:
        # Corners have two edges which don't match anything,
        # but we double all the edges ("normal" and "reverse" version)
        return len(set(edges) & corners_edges) == 4


    return internal


def get_corners(tiles: [tuple]) -> [tuple]:
    tiles_and_edges = {tile_id:all_possible_edges(tile) for tile_id, tile in tiles}
    count_edges = Counter(edge for edges in tiles_and_edges.values() for edge in edges)
    corners_edges = set(edge for edge, how_many_appear in count_edges.items() if how_many_appear == 1)

    is_corner = is_tile_a_corner(corners_edges)

    return (tile_id for tile_id, tile in tiles_and_edges.items() if is_corner(tile))


def solution_for_first_part(task_input) -> int:
    return reduce(mul, get_corners(parse(task_input)))


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


def solution_for_second_part(task_input):

    def get_and_orient_first_corner(corners: [Tile], border_edges: [int]) -> Tile:
        for n, w in permutations(set(corners[0].all_possible_edges) & border_edges, 2):
            if corners[0].orient_on_north_and_west(n, w):
                return corners[0]

        raise Exception('First corner not founded!')

    def find_for_first_row(used, edges, west):
        for tile in tiles:
            if tile.id in used:
                continue

            for north in tile.get_north_if_west(west):
                if north in edges:
                    tile.orient_on_north_and_west(north, west)
                    return tile

        raise Exception('Cannot find the tile for given edge')

    def find_for_first_column(used, edges, north):
        for tile in tiles:
            if tile.id in used:
                continue

            for west in tile.get_west_if_north(north):
                if west in edges:
                    tile.orient_on_north_and_west(north, west)
                    return tile

        raise Exception('Cannot find the tile for given edge')

    def match_tile(tiles, used, north, west):
        for tile in tiles:
            if tile.id not in used and tile.orient_on_north_and_west(north, west):
                return tile

        raise Exception('Cannot find the tile for given edge')

    def solve_jigsaw(tiles):
        jigsaw_size = floor(len(tiles) ** 0.5)
        border_edges = set(edge
            for edge, how_many_appear in Counter(edge for tile in tiles for edge in tile.all_possible_edges).items()
            if how_many_appear == 1)

        is_corner = is_tile_a_corner(border_edges)
        corners = [tile for tile in tiles if is_corner(tile.all_possible_edges)]

        solution = {FIRST_TILE: get_and_orient_first_corner(corners, border_edges)}
        used = set([solution[FIRST_TILE].id])

        previous = solution[FIRST_TILE]
        for x in range(1, jigsaw_size):
            current = find_for_first_row(used, border_edges, previous.current_edges[EAST])
            used.add(current.id)
            solution[(x, 0)] = current
            previous = current

        previous = solution[FIRST_TILE]
        for y in range(1, jigsaw_size):
            current = find_for_first_column(used, border_edges, previous.current_edges[SOUTH])
            used.add(current.id)
            solution[(0, y)] = current
            previous = current

        for y in range(1, jigsaw_size):
            for x in range(1, jigsaw_size):
                current = match_tile(tiles, used, solution[(x, y - 1)].current_edges[SOUTH], solution[(x - 1, y)].current_edges[EAST])
                solution[(x, y)] = current
                used.add(current.id)

        return solution, jigsaw_size

    def build_picture(solve_jigsaw: dict, jigsaw_size: int) -> set:
        bigger_picture = set()
        for y in range(0, jigsaw_size):
            for x in range(0, jigsaw_size):
                tile = solve_jigsaw[x, y]
                picture = transform(tile.transformations, tile.cut_edges(), PICTURE_SIZE_WITH_BORDERS)
                bigger_picture |= set((x * PICTURE_SIZE_WITH_BORDERS + p[0], y * PICTURE_SIZE_WITH_BORDERS + p[1]) for p in picture)

        return bigger_picture, jigsaw_size * PICTURE_SIZE_WITH_BORDERS

    def rotate_left_90(picture: set, size: int) -> set:
        return set(
            (size - y - 1, x)
            for x in range(0, size)
            for y in range(0, size)
            if (x, y) in picture)

    def flip_verticaly(picture: set, size: int) -> set:
        return set(
            (size - 1 - x, y)
            for x in range(0, size)
            for y in range(0, size)
            if (x, y) in picture)

    def flip_horizontaly(picture: set, size: int) -> set:
        return set(
            (x, size - 1 - y)
            for x in range(0, size)
            for y in range(0, size)
            if (x, y) in picture)

    def remove_subpictures_for_picture(picture, size, subpicture):
        subpicture_pixels = len(subpicture)
        subpicture_max_x = max(p[0] for p in subpicture)
        subpicture_max_y = max(p[1] for p in subpicture)
        found = False

        for y in range(0, size - subpicture_max_y):
            for x in range(0, size - subpicture_max_x):
                mask = set(
                    (x + sx, y + sy)
                    for sy in range(0, subpicture_max_y + 1)
                    for sx in range(0, subpicture_max_x + 1)
                    if (sx, sy) in subpicture)

                result = picture & mask
                if len(result) == subpicture_pixels:
                    found = True
                    picture -= mask

        return picture

    def transform(tranformations: str, picture, size):
        if not tranformations:
            return picture

        for tranformation in tranformations:
            if tranformation == 'r':
                picture = rotate_left_90(picture, size)
            elif tranformation == 'v':
                picture = flip_verticaly(picture, size)
            elif tranformation == 'h':
                picture = flip_horizontaly(picture, size)
            else:
                raise Exception('unknow transformaiton')

        return picture


    tiles = [Tile(tile_id, tile) for tile_id, tile in parse(task_input)]
    solution = solve_jigsaw(tiles)
    picture, picture_size = build_picture(*solution)

    monster = set(parse_image('''                  #
#    ##    ##    ###
 #  #  #  #  #  #   '''.splitlines()))

    pixels_number_before_removal = len(picture)
    for operation in ('', 'r', 'rr', 'rrr', 'v', 'vr', 'vrr', 'vrrr', 'h', 'hr', 'hrr', 'hrrr'):
        transformed_picture = transform(operation, picture, picture_size)
        pixels_with_monster = len(remove_subpictures_for_picture(transformed_picture, picture_size, monster))
        if pixels_with_monster < pixels_number_before_removal:
            return pixels_with_monster

    raise Exception('Monster not found!')


assert solution_for_second_part(example_input) == 273
print("Solution for the second part:", solution_for_second_part(task_input))
