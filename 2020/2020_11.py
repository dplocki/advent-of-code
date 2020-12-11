def load_input_file(file_name: str) -> [str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def all_neighbor():
    return list((x, y)
        for y in [- 1, 0, 1]
        for x in [- 1, 0, 1]
        if not (x == 0 and y == 0))


def simulate(task_input, iteration_generator):

    def parse(task_input: [str]) -> [tuple]:
        for y, line in enumerate(task_input):
            yield from ((x, y, c) for x, c in enumerate(line))


    seats = {(x, y): c for x, y, c in parse(task_input)}
    is_not_stable = True
    while is_not_stable:
        is_not_stable, seats = iteration_generator(seats) 

    return sum(1 for s in seats.values() if s == '#')


def solution_for_first_part(task_input):

    def count_occupied_seats(neighbor_coordinates):
        
        def internal(seats, coordinates):
            return sum(1 for x, y in neighbor_coordinates if seats.get((coordinates[0] + x, coordinates[1] + y), None) == '#')


        return internal


    def iteration_generator(count_occupied_seats_around):
       
        def internal(seats):
            new_layout = {}
            is_not_stable = False

            for coordinates, place in seats.items():
                if place == 'L' and count_occupied_seats_around(seats, coordinates) == 0:
                    is_not_stable = True
                    new_layout[coordinates] = '#'
                elif place == '#' and count_occupied_seats_around(seats, coordinates) >= 4:
                    is_not_stable = True
                    new_layout[coordinates] = 'L'
                else:
                    new_layout[coordinates] = place

            return is_not_stable, new_layout

        return internal


    return simulate(task_input, iteration_generator(count_occupied_seats(all_neighbor())))


example_input = '''L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL'''.splitlines()

assert solution_for_first_part(example_input) == 37

# The input is taken from: https://adventofcode.com/2020/day/11/input
task_input = list(load_input_file('input.11.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input):

    def how_occupied_around(memo, neighbors):

        def find_visible_seats(seats: dict, seat_from: tuple) -> [tuple]:
            sx, sy = seat_from
            for x, y in neighbors:
                d = 1
                while seats.get((sx + d * x, sy + d * y), None) == '.':
                    d += 1

                yield (sx + d * x, sy + d * y)


        def internal(seats, seat):
            if seat not in memo:
                memo[seat] = list(find_visible_seats(seats, seat))

            return list(seats.get(s, None) for s in memo[seat]).count('#')


        return internal


    def iteration_generator(how_occupied_around):

        def internal(seats):
            new_layout = {}
            is_not_stable = False

            for coordinates, place in seats.items():
                if place == 'L' and how_occupied_around(seats, coordinates) == 0:
                    is_not_stable = True
                    new_layout[coordinates] = '#'
                elif place == '#' and how_occupied_around(seats, coordinates) >= 5:
                    is_not_stable = True
                    new_layout[coordinates] = 'L'
                else:
                    new_layout[coordinates] = place

            return is_not_stable, new_layout


        return internal


    return simulate(task_input, iteration_generator(how_occupied_around({}, all_neighbor())))


assert solution_for_second_part(example_input) == 26
print("Solution for the second part:", solution_for_second_part(task_input))
