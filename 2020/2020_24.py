from itertools import chain


def load_input_file(file_name: str) -> [str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def get_black_tiles(instructions: [str]) -> set:
    result = set()
    for line in instructions:
        x, y, z = 0, 0, 0

        steps = list(line[::-1])
        while steps:
            step = steps.pop()
            if step == 'e':
                x, y, z = x + 1, y - 1, z
            elif step == 'w':
                x, y, z = x - 1, y + 1, z
            else:
                step += steps.pop()

                if step == 'se':
                    x, y, z = x, y - 1, z + 1
                elif step == 'sw':
                    x, y, z = x - 1, y, z + 1
                elif step == 'nw':
                    x, y, z = x, y + 1, z - 1
                elif step == 'ne':
                    x, y, z = x + 1, y, z - 1

        if (x, y, z) in result:
            result.discard((x, y, z))
        else:
            result.add((x, y, z))

    return result


def solution_for_first_part(task_input: [str]) -> int:
    return len(get_black_tiles(task_input))


example_input = '''sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew'''.splitlines()

assert solution_for_first_part(example_input) == 10

# The input is taken from: https://adventofcode.com/2020/day/24/input
task_input = list(load_input_file('input.24.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def get_neighorns(x: int, y: int, z: int) -> [tuple]:
    yield x, y + 1, z - 1
    yield x + 1, y, z - 1
    yield x + 1, y - 1, z
    yield x, y - 1, z + 1
    yield x - 1, y, z + 1
    yield x - 1, y + 1, z


def count_black_neighorns(black_tiles: set, coordinates: tuple) -> int:
    return sum(1 for neighorn in get_neighorns(*coordinates) if neighorn in black_tiles)


def will_be_black(black_tiles: set, coordinates: tuple) -> bool:
    black_neighbors_number = count_black_neighorns(black_tiles, coordinates)
    if coordinates in black_tiles:
        return 0 < black_neighbors_number <= 2
    else:
        return black_neighbors_number == 2


def solution_for_second_part(task_input: [str]) -> int:
    all_black = get_black_tiles(task_input)

    for _ in range(100):
        new_all_black = set()
        checked = set()

        for black_tile in all_black:
            for coordiantes in chain([black_tile], get_neighorns(*black_tile)):
                if coordiantes in checked:
                    continue

                checked.add(coordiantes)
                if will_be_black(all_black, coordiantes):
                    new_all_black.add(coordiantes)

        all_black = new_all_black

    return len(all_black)


assert solution_for_second_part(example_input) == 2208
print("Solution for the second part:", solution_for_second_part(task_input))
