from queue import Queue
from functools import cmp_to_key


X, Y = 0, 1
START_UNIT_HEALTH = 200
START_UNIT_ATTACK_POWER = 3


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
        occupied = find_occupied(walls, creatures)
        if not creature.is_alive():
            continue

        all_targests = [c for c in creatures if c.is_alive() and not c.is_same_race(creature)]
        if not all_targests:  # All enemies are death
            return True

        # Movement
        the_enemy_to_attacked = find_the_enemy_to_attacked(all_targests, creature.position)
        if not the_enemy_to_attacked:
            creature.position = find_the_next_step_position(occupied, all_targests, creature.position)
            occupied = find_occupied(walls, creatures)

        # Attack
        the_enemy_to_attacked = find_the_enemy_to_attacked(all_targests, creature.position)
        if the_enemy_to_attacked:
            the_enemy_to_attacked.recive_damage(creature)

    return False


def simulation(input: [str]):
    creatures, walls = analise_tokens(parse_lines(input))
    round_count = 0

    while True:
        is_end = round(walls, creatures)

        #print(round_count + 1)
        #visualisation(walls, creatures)

        if is_end:
            return sum([c.health for c in creatures if c.is_alive()]) * round_count
        else:
            round_count += 1


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


def simulation_test(input, excepted):
    result = simulation(input.splitlines())
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

simulation_test('''#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########''', 27828)

simulation_test('''#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######''', 27730)

simulation_test('''#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######''', 36334)

simulation_test('''#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######''', 39514)

simulation_test('''#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######''', 27755)

simulation_test('''#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######''', 28944)

simulation_test('''#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########''', 18740)

# The input taken from: https://adventofcode.com/2018/day/15/input
task_input = '''<input>'''.splitlines()

result = simulation(task_input)
print("Solution for first part:", result)
