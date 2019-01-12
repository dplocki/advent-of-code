import re
from copy import deepcopy


TESTING = False
IMMUNE_SYSTEM, INFECTION = 'Immune System', 'Infection'
IMMUNE, WEAK = 'immune', 'weak'


def calculate_recived_damage(attack_power, attack_type, defender_traits):
    result = attack_power

    if attack_type in defender_traits:
        if defender_traits[attack_type] == WEAK:
            result *= 2
        elif defender_traits[attack_type] == IMMUNE:
            result = 0

    return result


class Group:
    def __init__(self):
        self.name = None
        self.team = None
        self.units = 0
        self.hp_per_unit = 0
        self.attack = None
        self.attack_type = None
        self.initiative = 0
        self.traits = None

    def is_in_play(self):
        return self.units > 0

    def effective_power(self):
        return self.attack * self.units    

    def recived_damage(self, attacker):
        damage = calculate_recived_damage(attacker.effective_power(), attacker.attack_type, self.traits)
        self.units -= max(0, (damage // self.hp_per_unit))  # apperently sometimes damge can negative

    def __repr__(self):
        team = 'IMMUNE_SYSTEM' if self.team == IMMUNE_SYSTEM else 'INFECTION'
        x = self.effective_power()
        return f'{x} {team} {self.units}*{self.hp_per_unit} [i:{self.initiative}]'


def translate_input_to_object(lines: [str]):

    def parser_input(lines: [str]):
        pattern = re.compile(r'(\d+) units each with (\d+) hit points (\((.*?)\) )?with an attack that does (\d+) (.+) damage at initiative (\d+)')
        team = None

        for line in lines:
            if line == 'Immune System:':
                team = IMMUNE_SYSTEM
            elif line == 'Infection:':
                team = INFECTION
            elif line == '':
                continue
            else:
                match = pattern.match(line)
                yield team, int(match[1]), int(match[2]), match[4], int(match[5]), match[6], int(match[7])


    def parse_traits(traits):
        result = {}
        if traits:
            for trait in traits.split('; '):
                if trait.startswith('immune'):
                    for token in trait.replace('immune to ', '').split(', '):
                        result[token] = IMMUNE
                elif trait.startswith('weak'):
                    for token in trait.replace('weak to ', '').split(', '):
                        result[token] = WEAK

        return result

    
    infection_index = 1
    immune_system_index = 1

    groups = []
    for team, units, hp, raw_traits, damage, damage_type, initiative in parser_input(lines):
        group = Group()
        group.name = 'Group ' + str(infection_index if team == INFECTION else immune_system_index)
        group.team = team
        group.units = units
        group.hp_per_unit = hp
        group.attack = damage
        group.attack_type = damage_type
        group.initiative = initiative
        group.traits = parse_traits(raw_traits)
        groups.append(group)

        if team == IMMUNE_SYSTEM:
            immune_system_index += 1
        else:
            infection_index += 1

    return groups


def count_units_in_groups(groups: [Group]) -> int:
    return sum([g.units for g in groups])


def simulation(groups: [Group], boost_for_immune_system=0, verbose=False):


    def count_teams(groups):
        return len(set([g.team for g in groups]))


    def targeting_phase(groups: [Group]):


        def target_sorting(group: Group):
            return group.effective_power(), group.initiative


        def find_enemy_for_group(attacker, groups, attack_schedule: {Group: Group}):


            def visualisation_would_attack(enemies):
                if not verbose:
                    return

                for e, damage in enemies.items():
                    print(f'{attacker.team} {attacker.name} would deal defending {e.name} {damage} damage')


            def visualisation_will_not_attack():
                if not verbose:
                    return

                print(f'{attacker.team} {attacker.name} will not attack anyone')


            def visualisation_will_attack():
                if not verbose:
                    return

                print(f'{attacker.team} {attacker.name} will attack {enemies[0].name}')


            all_ready_taken = attack_schedule.values()
            enemies = {
                g: calculate_recived_damage(attacker.effective_power(), attacker.attack_type, g.traits)
                for g in groups
                if g.is_in_play() and g.team != attacker.team and g not in all_ready_taken
            }

            if enemies:
                visualisation_would_attack(enemies)

                maximum_damage = max(enemies.values())
                if maximum_damage > 0:
                    enemies = [e for e, v in enemies.items() if v == maximum_damage]
                    enemies.sort(key=target_sorting, reverse=True)

                    visualisation_will_attack()

                    return enemies[0]


            visualisation_will_not_attack()
            return None


        attack_schedule = {}
        groups.sort(key=target_sorting, reverse=True)
        for group in groups:
            attack_schedule[group] = find_enemy_for_group(group, groups, attack_schedule)

        return attack_schedule


    def attack_phase(groups: [Group], attack_schedule: {Group: Group}):
        groups.sort(key=lambda g: g.initiative, reverse=True)
        for attacker in groups:
            defender = attack_schedule[attacker]
            if defender:
                defender.recived_damage(attacker)

        return groups


    def visualisation_turn_begin(groups: [Group]):


        def active_groups_for_team(label, team):
            t = [g for g in groups if g.team == team]
            if not t:
                return
            t.sort(key=lambda x: x.name)
            print(label)
            for g in t:
                print(f'{g.name} contains {g.units} units [hp: {g.hp_per_unit}]')
            print()


        if not verbose:
            return

        print('\n------------------------------------------------------')
        active_groups_for_team('Immune system:', IMMUNE_SYSTEM)
        active_groups_for_team('Infection:', INFECTION)

    old_watch_dog = count_units_in_groups(groups)
    while True:
        groups = [g for g in groups if g.is_in_play()]

        visualisation_turn_begin(groups)
        if count_teams(groups) == 1:
            return groups

        attack_schedule = targeting_phase(groups)
        groups = attack_phase(groups, attack_schedule)

        new_watch_dog = count_units_in_groups(groups)
        if new_watch_dog == old_watch_dog:
            return None
        else:
            old_watch_dog = new_watch_dog



def first_part_solution(input: [str], verbose=False):
    groups = translate_input_to_object(input)
    winnig_groups = simulation(groups, verbose=verbose)
    return count_units_in_groups(winnig_groups)


def second_part_solution(input: [str], verbose=False):

    def test(groups, boost):
        for g in groups:
            if g.team == IMMUNE_SYSTEM:
                g.attack += boost

        winnig_groups = simulation(groups, verbose=verbose)
        if winnig_groups:
            if verbose:
                print("Testing boost =", boost, "result: ", winnig_groups[0].team == IMMUNE_SYSTEM)

            return winnig_groups[0].team == IMMUNE_SYSTEM, sum([g.units for g in winnig_groups])
        else:
            if verbose:
                print("Testing boost =", boost, "result: deadlock")

            return False, None


    original_groups = translate_input_to_object(input)
    bad = 0
    good = 10000
    last_good_units_number = None

    while bad + 1 != good:  # For some inputs its also bad solution, as in solution for AoC 2018#15, but works for mine, I like this binary search
        local_boost = bad + ((good - bad) // 2)
        test_result, units_number = test(deepcopy(original_groups), local_boost)
        if test_result:
            good = local_boost
            last_good_units_number = units_number
        else:
            bad = local_boost

    return last_good_units_number



if TESTING:

    test_lines = '''Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4'''

    assert first_part_solution(test_lines.splitlines(), verbose=False) == 5216
    assert second_part_solution(test_lines.splitlines(), verbose=False) == 51

else:
    def read_input_file(file_name) -> [int]:
        with open(file_name) as file:
            for line in file:
                yield line.rstrip('\n')

    # The input taken from: https://adventofcode.com/2018/day/24/input
    print("Solution for the first part:", first_part_solution(read_input_file('input.24.txt'), verbose=False))
    print("Solution for the second part:", second_part_solution(read_input_file('input.24.txt'), verbose=False))
