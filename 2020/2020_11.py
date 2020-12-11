def load_input_file(file_name: str) -> [str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: [str]) -> [tuple]:
    for y, line in enumerate(task_input):
        yield from ((x, y, c) for x, c in enumerate(line))


def solution_for_first_part(task_input):

    def all_neighbor():
        return list((x, y)
            for y in [- 1, 0, 1]
            for x in [- 1, 0, 1]
            if not (x == 0 and y == 0))


    def count_occupied_seats(neighbor_coordinates):
        
        def internal(seats, coordinates):
            return sum(1 for x, y in neighbor_coordinates if seats.get((coordinates[0] + x, coordinates[1] + y), '.') == '#')


        return internal


    count_occupied_seats_around = count_occupied_seats(all_neighbor())
    seats = {(x, y): c for x, y, c in parse(task_input)}

    is_not_stable = True
    while is_not_stable:
        is_not_stable = False
        new_layout = {}

        for coordinates, place in seats.items():
            if place == 'L' and count_occupied_seats_around(seats, coordinates) == 0:
                is_not_stable = True
                new_layout[coordinates] = '#'
            elif place == '#' and count_occupied_seats_around(seats, coordinates) >= 4:
                is_not_stable = True
                new_layout[coordinates] = 'L'
            else:
                new_layout[coordinates] = place

        seats = new_layout

    return sum(1 for s in seats.values() if s == '#')



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
task_input = load_input_file('input.11.txt')
result = solution_for_first_part(task_input)
print("Solution for the first part:", result)
