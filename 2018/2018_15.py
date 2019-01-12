from queue import Queue
from functools import cmp_to_key
from copy import deepcopy


TESTING = False

X, Y = 0, 1
START_UNIT_HEALTH = 200
START_UNIT_ATTACK_POWER = 3
ELVE, GOBLIN = 'E', 'G'


def parse_lines(input: [str]):
    for y, line in enumerate(input):
        for x, ch in enumerate(line):
            if ch != '.':
                yield (x, y), ch


def reading_order(a, b):
    if a[Y] == b[Y]:
        return a[X] - b[X]

    return a[Y] - b[Y]


class Creature:
    def __init__(self, race):
        self.race = race
        self.position = None
        self.health = START_UNIT_HEALTH
        self.attact_power = START_UNIT_ATTACK_POWER

    def is_alive(self):
        return self.health > 0

    def is_same_race(self, other):
        return self.race == other.race

    def recive_damage(self, creature):
        self.health -= creature.attact_power

    def __lt__(self, other):
        return reading_order(self.position, other.position) < 0

    def __repr__(self):
        return f'{self.race}({self.health}) [{self.position[X]}x{self.position[Y]}]'


def analise_tokens(parser):
    creatures = []
    walls = set()

    for position, what in parser:
        if what == '#':
            walls.add(position)
        elif what in 'EG':
            creature = Creature(what)
            creature.position = position
            creatures.append(creature)

    return creatures, walls


def neighbors_positions(position):
    return [
        (position[X] + x, position[Y] + y)
        for x, y in [(0, -1), (-1, 0), (1, 0), (0, 1)]
    ]


def neighbors_not_occupied_positions(position, occupied):
    return [p for p in neighbors_positions(position) if not p in occupied]


def find_the_shortest_path_to_enemies(_from, attacked_positions, occupied):
    # Big thanks for this: https://www.redblobgames.com/pathfinding/a-star/introduction.html
    frontier = Queue()
    frontier.put(_from)
    cost_so_far = {_from: 0}
    first_step = {p: p for p in neighbors_not_occupied_positions(_from, occupied)}
    results = {}

    while not frontier.empty():
        current = frontier.get()
        if current in attacked_positions:
            results[current] = (cost_so_far[current], first_step[current])

        new_cost = cost_so_far[current] + 1
        for next in neighbors_not_occupied_positions(current, occupied):
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                frontier.put(next)
                cost_so_far[next] = new_cost
                if current != _from:
                    first_step[next] = first_step[current]

    return results


def find_the_enemy_to_attacked(all_targests: [], start_position):
    all_targests_positions = {target.position: target for target in all_targests}
    result = [
        all_targests_positions[tmp]
        for tmp in neighbors_positions(start_position)
        if tmp in all_targests_positions
    ]

    if result:
        return min(result, key=lambda p: p.health)
    else:
        return None


def find_the_next_step_position(occupied, all_targests, start_position):
    attacked_positions = [target_point for target in all_targests for target_point in neighbors_not_occupied_positions(target.position, occupied)]
    findings = find_the_shortest_path_to_enemies(start_position, attacked_positions, occupied)

    if findings:
        the_shortest_path = min(findings.values(), key=lambda x: x[0])[0]
        targets = [k for k, v in findings.items() if v[0] == the_shortest_path]
        targets.sort(key=cmp_to_key(reading_order))

        return findings[targets[0]][1]

    return start_position


def find_occupied(walls, creatures):
    return walls.union([c.position for c in creatures if c.is_alive()])


def round(walls: set, creatures: [Creature]):
    creatures.sort()
    for creature in creatures:
        if not creature.is_alive():
            continue

        occupied = find_occupied(walls, creatures)

        all_targests = [c for c in creatures if c.is_alive() and not c.is_same_race(creature)]
        if not all_targests:  # All enemies are death
            return True

        # Movement
        the_enemy_to_attacked = find_the_enemy_to_attacked(all_targests, creature.position)
        if not the_enemy_to_attacked:
            creature.position = find_the_next_step_position(occupied, all_targests, creature.position)
            the_enemy_to_attacked = find_the_enemy_to_attacked(all_targests, creature.position)

        # Attack
        if the_enemy_to_attacked:
            the_enemy_to_attacked.recive_damage(creature)

    return False


def simulation(creatures, walls, extra_exit=None, verbose=False):
    round_count = 0

    while True:
        is_end = round(walls, creatures)

        if verbose:
            print(round_count + 1)
            visualisation(walls, creatures)

        if (extra_exit and extra_exit(creatures)) or is_end:
            return round_count, creatures
        else:
            round_count += 1


def run_simulation(input: [str], verbose=False):
    return simulation(*analise_tokens(parse_lines(input)), verbose=verbose)


def run_first_part_simulation(input: str, verbose=False):
    round_count, creatures = run_simulation(input.splitlines(), verbose=verbose)
    living = [c.health for c in creatures if c.is_alive()]
    return sum(living) * round_count


def visualisation(walls: set, creatures: []):
    def find_creature_for_position(position):
        for c in creatures:
            if c.is_alive() and (x, y) == c.position:
                return c

        return None

    size_x = max(walls, key=lambda p: p[X])[X]
    size_y = max(walls, key=lambda p: p[Y])[Y]

    for y in range(size_y + 1):
        cs = []

        for x in range(size_x + 1):
            if (x, y) in walls:
                print('#', end='')
            else:
                c = find_creature_for_position((x, y))
                if c:
                    cs.append(c)
                    print(c.race, end='')
                else:
                    print('.', end='')

        if cs:
            print('\t', end='')
            for c in cs:
                print(f'{c.race}({c.health}) ', end='')

        print('\n', end='')


def find_the_first_good(input, verbose=False):
    '''This method originaly use bisect algorithm, but for my input, you can't use it

        Testing: 4 -> result: 109894 all elves survive: False
        Testing: 5 -> result: 106352 all elves survive: False
        Testing: 6 -> result: 102879 all elves survive: False
        Testing: 7 -> result: 100924 all elves survive: False
        Testing: 8 -> result: 96370 all elves survive: False
        Testing: 9 -> result: 93794 all elves survive: False
        Testing: 10 -> result: 91080 all elves survive: False
        Testing: 11 -> result: 88464 all elves survive: False
        Testing: 12 -> result: 84240 all elves survive: False
        Testing: 13 -> result: 82782 all elves survive: False
        Testing: 14 -> result: 77224 all elves survive: False
        Testing: 15 -> result: 65000 all elves survive: False
        Testing: 16 -> result: 62468 all elves survive: True
        Testing: 17 -> result: 66384 all elves survive: False
        Testing: 18 -> result: 65904 all elves survive: False
        Testing: 19 -> result: 59052 all elves survive: True
        Testing: 20 -> result: 65164 all elves survive: True    
    '''

    def check_if_elve_died(creatures):
        return len([c for c in creatures if c.race == ELVE and not c.is_alive()]) > 0

    def test_of_attack_power(initial_creatures, initial_walls, new_attack_power):
        for creature in initial_creatures:
            if creature.race == ELVE:
                creature.attact_power = new_attack_power

        round_count, end_creatures = simulation(initial_creatures, initial_walls, extra_exit=check_if_elve_died)
        living = [c for c in end_creatures if c.is_alive()]
        result = len([c for c in end_creatures if not c.is_alive() and c.race == ELVE])

        return result == 0, sum([l.health for l in living]) * round_count

    creatures, walls = analise_tokens(parse_lines(input.splitlines()))
    new_attack_power = 4
    while True:
        elves_win, result = test_of_attack_power(deepcopy(creatures), walls, new_attack_power)

        if verbose:
            print(f"Testing: {new_attack_power} -> result: {result} all elves survive: {elves_win}")

        if elves_win:
            return result
        else:
            new_attack_power += 1


if TESTING:

    def run_first_part_simulation_test(input, excepted):
        result = run_first_part_simulation(input)
        assert result == excepted, f"Excepted: {excepted}, recived: {result}"


    test_input_1 = '''#######
#...#.#
#.#G..#
#..##.#
#..G#.#
#...#E#
#######'''.splitlines()

    test_input_2 = '''#######
#.E...#
#.....#
#...G.#
#######'''.splitlines()

    assert neighbors_not_occupied_positions((1, 1), [(0, 1), (1, 0), (2, 1), (1, 2)]) == []
    assert neighbors_not_occupied_positions((1, 1), [(0, 1), (1, 0), (2, 1)]) == [(1, 2)]
    assert len(neighbors_not_occupied_positions((1, 1), [])) == 4

    test_creatures_1, test_walls_1 = analise_tokens(parse_lines(test_input_1))
    test_occupied_1 = find_occupied(test_walls_1, test_creatures_1)

    assert find_the_next_step_position(test_occupied_1, [test_creatures_1[0]], (5, 5)) == (5, 4)
    assert find_the_next_step_position(test_occupied_1, [test_creatures_1[0]], (5, 4)) == (5, 3)
    assert find_the_next_step_position(test_occupied_1, [test_creatures_1[0]], (5, 3)) == (5, 2)
    assert find_the_next_step_position(test_occupied_1, [test_creatures_1[0]], (5, 2)) == (4, 2)

    test_creatures_2, test_walls_2 = analise_tokens(parse_lines(test_input_2))
    test_occupied_2 = find_occupied(test_walls_2, test_creatures_2)

    assert find_the_next_step_position(test_occupied_2, [test_creatures_2[1]], (2, 1)) == (3, 1)

    run_first_part_simulation_test('''#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########''', 27828)

    run_first_part_simulation_test('''#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######''', 27730)

    run_first_part_simulation_test('''#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######''', 36334)

    run_first_part_simulation_test('''#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######''', 39514)

    run_first_part_simulation_test('''#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######''', 27755)

    run_first_part_simulation_test('''#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######''', 28944)

    run_first_part_simulation_test('''#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########''', 18740)


    def find_the_first_good_test(input, excepted_result, excepted_attack_power):
        actual = find_the_first_good(input)
        assert actual == excepted_result, f'Result excepted: {excepted_result}, recived: {actual}'


    find_the_first_good_test('''#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######''', 4988, 15)

    find_the_first_good_test('''#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######''', 31284, 4)

    find_the_first_good_test('''#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######''', 3478, 15)

    find_the_first_good_test('''#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######''', 6474, 12)

    find_the_first_good_test('''#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########''', 1140, 34)

else:
    # The input taken from: https://adventofcode.com/2018/day/15/input
    task_input = '''<input>'''

    print("Solution for the first part:", run_first_part_simulation(task_input))
    print("Solution for the second part:", find_the_first_good(task_input))
