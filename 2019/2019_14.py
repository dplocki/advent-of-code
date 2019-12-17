import math


ORE = 'ORE'
FUEL = 'FUEL'


def load_input_file(file_name):
    with open(file_name) as file:
        yield from [line.strip() for line in file]


def build_recipty(lines):

    def parse_ingredient(raw_input):
        number, name = raw_input.split(' ')
        return int(number), name


    def parse_recipes(lines: [str]):
        for line in lines:
            raw_needed, raw_result = line.split(' => ')

            yield list(map(parse_ingredient, raw_needed.split(', '))), parse_ingredient(raw_result)

    return {result[1]:(result[0], ingridient_list) for ingridient_list, result in parse_recipes(lines)}


def how_much_ore_need(reaction_graph, what, how_much, leftovers):
    if what in leftovers:
        if leftovers[what] >= how_much:
            leftovers[what] -= how_much
            return 0, leftovers
        else:
            how_much -= leftovers[what]
            leftovers[what] = 0

    if what == ORE:
        return how_much, leftovers

    will_produce, ingreedients = reaction_graph[what]
    multiplayer = max(1, math.ceil(how_much / will_produce))

    ore_need = 0
    for q, n in ingreedients:
        o, leftovers = how_much_ore_need(reaction_graph, n, q * multiplayer, leftovers)
        ore_need += o

    leftovers[what] = leftovers.get(what, 0) + will_produce * multiplayer - how_much

    return ore_need, leftovers


def solution_for_first_part(reaction_graph):
    ore_per_fuel, _ = how_much_ore_need(reaction_graph, FUEL, 1, {})
    return ore_per_fuel


input_31_ore = '''10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL'''.splitlines()

input_165_ore = '''9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL'''.splitlines()

input_13312_ore = '''157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT'''.splitlines()

input_180697_ore = '''2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF'''.splitlines()

input_2210736_ore = '''171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX'''.splitlines()


assert solution_for_first_part(build_recipty(input_31_ore)) == 31
assert solution_for_first_part(build_recipty(input_165_ore)) == 165
assert solution_for_first_part(build_recipty(input_13312_ore)) == 13312
assert solution_for_first_part(build_recipty(input_180697_ore)) == 180697
assert solution_for_first_part(build_recipty(input_2210736_ore)) == 2210736

# The input is taken from: https://adventofcode.com/2019/day/14/input
reaction_graph = build_recipty(load_input_file('input.14.txt'))
ore_per_fuel = solution_for_first_part(reaction_graph)
print("Solution for the first part:", ore_per_fuel)


def solution_for_second_part(reaction_graph, ore_per_fuel):
    trylion = 1_000_000_000_000
    right = trylion
    left = trylion // ore_per_fuel
    best = 0

    while left <= right:
        mid = (left + right) // 2

        ore_need, _ = how_much_ore_need(reaction_graph, FUEL, mid, {})
        if ore_need < trylion:
            best = max(best, mid)
            left = mid + 1
        elif ore_need > trylion:
            right = mid - 1
        else:
            return mid

    return best


assert solution_for_second_part(build_recipty(input_13312_ore), 13312) == 82892753
assert solution_for_second_part(build_recipty(input_180697_ore), 180697) == 5586022
assert solution_for_second_part(build_recipty(input_2210736_ore), 2210736) == 460664

print("Solution for the second part:", solution_for_second_part(reaction_graph, ore_per_fuel))
