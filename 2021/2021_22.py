import re


def load_input_file(file_name: str) -> list[str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: list[str]) -> list[tuple[str, int, int, int, int, int, int]]:
    pattern = re.compile(r'(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)')

    for line in task_input:
        groups = pattern.match(line)
        yield groups[1], int(groups[2]), int(groups[3]), int(groups[4]), int(groups[5]), int(groups[6]), int(groups[7])


def solution_for_first_part(task_input: list[str]) -> int:
    reactors = set()
    s = list(parse(task_input))

    for state, xs, xe, ys, ye, zs, ze in s:
        xs = max(-50, xs)
        xe = min(50, xe)
        ys = max(-50, ys)
        ye = min(50, ye)
        zs = max(-50, zs)
        ze = min(50, ze)

        for x in range(xs, xe + 1):
            for y in range(ys, ye + 1):
                for z in range(zs, ze + 1):
                    reactor = (x, y, z)
                    if state == 'on':
                        reactors.add(reactor)
                    else:
                        if reactor in reactors:
                            reactors.remove(reactor)

    return len(reactors)


example_input = '''on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682'''.splitlines()

assert solution_for_first_part(example_input) == 590784
# The input is taken from: https://adventofcode.com/2021/day/22/input
task_input = list(load_input_file('input.22.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
