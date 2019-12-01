import itertools
from functools import reduce
from copy import deepcopy


ELEVATOR = 999
FIRST_FLOOR = 1
LAST_FLOOR = 4


def load_file(file_name: str):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def load_data(lines: [str]):

    def parse(lines: [str]):
        floor = FIRST_FLOOR

        for line in lines:
            _, items_raw = line.split(' floor contains ')
            yield floor, map(
                        lambda x: x.strip(),
                        filter(
                            None,
                            items_raw[:-1]
                                .replace(' and', '')
                                .replace(',', '')
                                .replace('-compatible', '')
                                .split('a ')
                        )
                    ) if items_raw != 'nothing relevant.' else []
            floor += 1

    result = {
            floor: list([tuple(c.split(' ')) for c in content])
            for floor, content in parse(lines)
        }

    result[ELEVATOR] = FIRST_FLOOR

    return result


def find_the_fastest_way(facility_map: {int: []}):

    def check_if_finished(facility_map):
        return sum(len(floor_content) for floor_number, floor_content in facility_map.items() if floor_number < LAST_FLOOR) == 0

    def is_microchip_fry(floor_items):
        generators = [g[0] for g in floor_items if g[1] == 'generator']

        return len(generators) > 0 and len([fi for fi in floor_items if fi[1] == 'microchip' and not fi[0] in generators]) > 0

    def calculate_hash(facility_map: {int: []}):
        microchips = {}
        for floor in range(FIRST_FLOOR, LAST_FLOOR + 1):
            for fi in facility_map[floor]:
                if fi[1] == 'microchip':
                    microchips[fi[0]] = floor

        result = str(facility_map[ELEVATOR])
        for floor in range(FIRST_FLOOR, LAST_FLOOR + 1):
            generators = [str(microchips[fi[0]]) for fi in facility_map[floor] if fi[1] == 'generator']
            generators.sort()

            result += ':' + str(floor) + ''.join(generators)

        return result

    def get_posibilities(facility_map: {int: []}):
        floor_content = facility_map[facility_map[ELEVATOR]]
 
        for selected_items in itertools.chain(itertools.combinations(floor_content, 2), map(lambda x: [x], floor_content)):
            on_floor_left = [fc for fc in floor_content if not fc in selected_items]
            if is_microchip_fry(on_floor_left):
                continue

            # up
            if facility_map[ELEVATOR] < LAST_FLOOR:
                new_floor_content = facility_map[facility_map[ELEVATOR] + 1] + list(selected_items)
                if not is_microchip_fry(new_floor_content):
                    new_facility_map = deepcopy(facility_map)
                    new_facility_map[facility_map[ELEVATOR]] = on_floor_left
                    new_facility_map[ELEVATOR] += 1
                    new_facility_map[new_facility_map[ELEVATOR]] = new_floor_content
                    yield new_facility_map

            # down
            if facility_map[ELEVATOR] > FIRST_FLOOR:
                new_floor_content = facility_map[facility_map[ELEVATOR] - 1] + list(selected_items)
                if not is_microchip_fry(new_floor_content):
                    new_facility_map = deepcopy(facility_map)
                    new_facility_map[facility_map[ELEVATOR]] = on_floor_left
                    new_facility_map[ELEVATOR] -= 1
                    new_facility_map[new_facility_map[ELEVATOR]] = new_floor_content
                    yield new_facility_map

    been = set()
    posibilities = [(0, facility_map)]
    while posibilities:
        steps_number, new_facility_map = posibilities.pop(0)

        if check_if_finished(new_facility_map):
            return steps_number

        for next in get_posibilities(new_facility_map):
            hash = calculate_hash(next)
            if hash in been:
                continue

            been.add(hash)
            posibilities.append((steps_number + 1, next))


def test_of_find_the_fastest_way(input, expected):
    result = find_the_fastest_way(load_data(input))
    assert result == expected, f"Expected {expected}, recived: {result}"


test_of_find_the_fastest_way('''The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.'''.splitlines(), 11)

# The input is taken from: https://adventofcode.com/2016/day/11/input
facility_map = load_data(load_file('input.11.txt'))
print("Solution for the first part:", find_the_fastest_way(facility_map))

facility_map[FIRST_FLOOR].append(('elerium', 'generator'))
facility_map[FIRST_FLOOR].append(('dilithium', 'generator'))
facility_map[FIRST_FLOOR].append(('elerium', 'microchip'))
facility_map[FIRST_FLOOR].append(('dilithium', 'microchip'))

print("Solution for the second part:", find_the_fastest_way(facility_map))
