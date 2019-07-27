import copy
import itertools


class Fighter():
    def __init__(self, name, hit_points=0, damage = 0, armor = 0):
        self.name = name
        self.hit_points = hit_points
        self.damage = damage
        self.armor = armor


def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)

def parse_input_to_fighter_class(input_lines):
    result = Fighter(name = 'boss')

    for line in input_lines:
        tokens = line.split(': ')
        setattr(result, tokens[0].lower().replace(' ', '_'), int(tokens[1]))
    
    return result


def check_if_player_wins(player: Fighter, boss: Fighter, show_logs = False):

    def enemy_died_becouse_of_attack(attacker, defender):
        damage = max(1, attacker.damage - defender.armor)
        defender.hit_points -= damage

        if show_logs:
            print(f'The {attacker.name} deals {attacker.damage}-{defender.armor} = {damage} damage; the {defender.name} goes down to {defender.hit_points} hit points.')

        return defender.hit_points <= 0

    while True:
        if enemy_died_becouse_of_attack(player, boss):
            return True

        if enemy_died_becouse_of_attack(boss, player):
            return False


def items_sets_generator():

    def build_set(weapon, armor, ring_a, ring_b):
        return (
                weapon[0] + armor[0] + ring_a[0] + ring_b[0],
                weapon[1] + armor[1] + ring_a[1] + ring_b[1],
                weapon[2] + armor[2] + ring_a[2] + ring_b[2])

    weapons = [
        [8, 4, 0],
        [10, 5, 0],
        [25, 6, 0],
        [40, 7, 0],
        [74, 8, 0],
    ]

    armors = [
        [0, 0, 0],
        [13, 0, 1],
        [31, 0, 2],
        [53, 0, 3],
        [75, 0, 4],
        [102, 0, 5]
    ]

    rings = [
        [25, 1, 0],
        [50, 2, 0],
        [100, 3, 0],
        [20, 0, 1],
        [40, 0, 2],
        [80, 0, 3]
    ]

    no_ring = [0, 0, 0]

    for weapon in weapons:
        for armor in armors:
            yield build_set(weapon, armor, no_ring, no_ring)

            for ring in rings:
                yield build_set(weapon, armor, ring, no_ring)

            for ring_a, ring_b in itertools.combinations(rings, 2):
                yield build_set(weapon, armor, ring_a, ring_b)


def only_prices_of_items_sets_with_result(items_sets_generator: [], boss: Fighter, result) -> []:
    for items_set in items_sets_generator:
        player = Fighter(name='player', hit_points = 100, damage=items_set[1], armor=items_set[2])
        tmp_boss = copy.copy(boss)

        if check_if_player_wins(player, tmp_boss) == result:
            yield items_set[0]


test_player = Fighter('player', hit_points=8, damage=5, armor=5)
test_boss = Fighter('boss', hit_points=12, damage=7, armor=2)
assert check_if_player_wins(test_player, test_boss) == True

# The input is taken from: https://adventofcode.com/2015/day/21/input
boss = parse_input_to_fighter_class(load_input_file('input.21.txt'))
all_items_sets = list(items_sets_generator())

print("Solution for the first part:", min(only_prices_of_items_sets_with_result(all_items_sets, boss, True)))
print("Solution for the second part:", max(only_prices_of_items_sets_with_result(all_items_sets, boss, False)))
