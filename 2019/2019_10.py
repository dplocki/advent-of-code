X = 0
Y = 1


def load_input_file(file_name: str):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse_input(lines: [str]):
    result = []
    y = 0
    for line in lines:
        result.extend([(x, y) for x, n in enumerate(line) if n != '.'])
        y += 1

    return result


def get_numer_of_visible(asteroids_list: [(int, int)], asteroid: [(int, int)]) -> int:

    def find_all_in_line_with(other_asteroids_list, asteroid, other_asteroid):
        dx = other_asteroid[X] - asteroid[X]
        dy = other_asteroid[Y] - asteroid[Y]
        delta = dy / dx

        return [a for a in other_asteroids_list if (a[Y] - asteroid[Y]) / (a[X] - asteroid[X]) == delta]

    def count_in_line(other_asteroids_list, asteroids_in_line, result, coordinate=X):
        if len(asteroids_in_line) > 0:
            if len([a for a in asteroids_in_line if a[coordinate] < asteroid[coordinate]]) > 0:
                result += 1

            if len([a for a in asteroids_in_line if a[coordinate] > asteroid[coordinate]]) > 0:
                result += 1

            other_asteroids_list = [a for a in other_asteroids_list if not a in asteroids_in_line]
        
        return other_asteroids_list, result

    result = 0
    other_asteroids_list = [a for a in asteroids_list if a != asteroid]
    other_asteroids_list, result = count_in_line(other_asteroids_list, [a for a in other_asteroids_list if a[X] == asteroid[X]], result, Y)
    other_asteroids_list, result = count_in_line(other_asteroids_list, [a for a in other_asteroids_list if a[Y] == asteroid[Y]], result)

    while other_asteroids_list:
        asteroids_in_line = find_all_in_line_with(other_asteroids_list, asteroid, other_asteroids_list[0])
        other_asteroids_list, result = count_in_line(other_asteroids_list, asteroids_in_line, result)

    return result


def solution_for_first_part(asteroids_map: [str]) -> int:
    asteroids_list = parse_input(asteroids_map)
    visibility_map = {n: get_numer_of_visible(asteroids_list[:], n) for n in asteroids_list}

    location = max(visibility_map, key=visibility_map.get)
    return location, visibility_map[location]


def test_of_first_part(test_input: str, expected_position: (int, int), expected_result: int):
    position, result = solution_for_first_part(test_input.splitlines())

    assert position == expected_position, f"Invalid position: expected {expected_position} recived: {position}"
    assert result == expected_result, f"Invalid result: expected {expected_result} recived: {result}"


test_of_first_part('''......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####''', (5, 8), 33)

test_of_first_part('''#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.''', (1, 2), 35)

test_of_first_part('''.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..''', (6, 3), 41)

large_test_input = '''.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##'''

large_test_input_excepted_position = (11,13)
test_of_first_part(large_test_input, large_test_input_excepted_position, 210)

# The input is taken from: https://adventofcode.com/2019/day/10/input
asteroids_list = list(load_input_file('input.10.txt'))
station_location, how_many_visible = solution_for_first_part(asteroids_list)
print("Solution for the first part:", how_many_visible)


def vaporize_asteroid(asteroids_list: [(int, int)], starting_point: []) -> [(int, int)]:

    POINT = 0
    DELTA = 1
    X_DELTA = 2
    Y_DELTA = 3


    def select_targets(not_vaporized_yet: [((int, int), float, int, int)], canton_select) -> [((int, int), float, int, int)]:
        canton = [am for am in not_vaporized_yet if canton_select(am)]
        result = None

        if len(canton) > 0:
            deltas = {}
            for a in canton:
                deltas[a[DELTA]] = deltas.get(a[DELTA], []) + [a]

            deltas = {v:sorted(k, key=lambda x: x[X_DELTA]) for v, k in deltas.items()}

            result = [deltas[k][0][0] for k in sorted(deltas.keys(), key=lambda a: a)]
            not_vaporized_yet = [a for a in not_vaporized_yet if not a in result]
    
        return not_vaporized_yet, result or []


    def select_targets_in_line(not_vaporized_yet: [((int, int), float, int, int)], selector) -> ((int, int), float, int, int):
        quater = [am for am in not_vaporized_yet if selector(am)]
        if len(quater) > 0:
            index = Y_DELTA if quater[0][X_DELTA] == 0 else X_DELTA
            result = min(quater, key=lambda a:abs(a[index]))
            return [a for a in not_vaporized_yet if a != result], [result[POINT]]
        
        return not_vaporized_yet, []


    not_vaporized_yet = [
            (
                a,
                (a[Y] - starting_point[Y]) / (a[X] - starting_point[X]) if a[X] - starting_point[X] else None,
                a[X] - starting_point[X], 
                a[Y] - starting_point[Y]
            )
            for a in asteroids_list
            if a != starting_point
        ]
    
    cannon_path = [
        (select_targets_in_line, lambda am: am[X_DELTA] == 0 and am[Y_DELTA] < 0),
        (select_targets, lambda am: am[X_DELTA] > 0 and am[Y_DELTA] < 0),
        (select_targets_in_line, lambda am: am[X_DELTA] > 0 and am[Y_DELTA] == 0),
        (select_targets, lambda am: am[X_DELTA] > 0 and am[Y_DELTA] > 0),
        (select_targets_in_line, lambda am: am[X_DELTA] == 0 and am[Y_DELTA] > 0),
        (select_targets, lambda am: am[X_DELTA] < 0 and am[Y_DELTA] > 0),
        (select_targets_in_line, lambda am: am[X_DELTA] < 0 and am[Y_DELTA] == 0),
        (select_targets, lambda am: am[X_DELTA] < 0 and am[Y_DELTA] < 0),
    ]

    while not_vaporized_yet:
        for select_for_canton, selector in cannon_path:
            not_vaporized_yet, vaporized = select_for_canton(not_vaporized_yet, selector)
            yield from vaporized
       

def solution_for_second_part(asteroids_map, station_location):
    asteroids_list = parse_input(asteroids_map)
    for _, v in zip(range(200), vaporize_asteroid(asteroids_list, station_location)):
        v

    return v[X] * 100 + v[Y]


assert solution_for_second_part(large_test_input.splitlines(), large_test_input_excepted_position) == 802

print("Solution for the second part:", solution_for_second_part(asteroids_list, station_location))
