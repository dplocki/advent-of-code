X = 0
Y = 1


def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse_input(f):
    result = []
    y = 0
    for l in f:
        result.extend([(x, y) for x, n in enumerate(l) if n != '.'])
        y += 1

    return result


def get_numer_of_visible(asteroids_list, asteroid):

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

    return visibility_map[max(visibility_map, key=visibility_map.get)]


test_map_1 = '''.#..#
.....
#####
....#
...##'''.splitlines()

test_map_2 = '''......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####'''.splitlines()

assert solution_for_first_part(test_map_1) == 8
assert solution_for_first_part(test_map_2) == 33

# The input is taken from: https://adventofcode.com/2019/day/10/input
asteroids_list = load_input_file('input.10.txt')
print("Solution for the first part:", solution_for_first_part(asteroids_list))
