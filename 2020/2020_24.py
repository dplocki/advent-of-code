def load_input_file(file_name: str) -> [str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def solution_for_first_part(task_input):
    lines = list(task_input)

    all_tiles = {}
    for line in lines:
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

        all_tiles[(x, y, z)] = not all_tiles.get((x, y, z), True)

    return sum(1 for i in all_tiles.values() if not i)


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
