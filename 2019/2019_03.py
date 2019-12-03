def load_input_file(file_name):

    def load(file_name):
        with open(file_name) as file:
            yield from (line.strip() for line in file)

    return list(load(file_name))


def position_the_line(line, been, count_function):
    x, y = 0, 0
    steps_counter = 0

    for i in line.split(','):
        direction = i[0]
        how_long = int(i[1:])

        if direction == 'R' or direction == 'L':
            step = 1 if direction == 'R' else -1
            for _ in range(0, how_long):
                x += step
                steps_counter += 1
                count_function(been, (x, y), steps_counter)
        else:
            step = 1 if direction == 'U' else -1
            for _ in range(0, how_long):
                y += step
                steps_counter += 1
                count_function(been, (x, y), steps_counter)

    return been


def solution_for_first_part(input_lines):

    def find_intersections(been, point, _):
        been[point] = been.get(point, 0) + 1

    been = position_the_line(input_lines[0], {}, find_intersections)
    been = {k: 1 for k, _ in been.items()}
    position_the_line(input_lines[1], been, find_intersections)

    return min([abs(k[0]) + abs(k[1]) for k, v in been.items() if v > 1])


assert solution_for_first_part('''R8,U5,L5,D3
U7,R6,D4,L4'''.splitlines()) == 6

assert solution_for_first_part('''R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'''.splitlines()) == 135

assert solution_for_first_part('''R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83'''.splitlines()) == 159

# The input is taken from: https://adventofcode.com/2019/day/3/input
input_lines = load_input_file('input.03.txt')
print("Solution for the first part:", solution_for_first_part(input_lines))


def solution_for_second_part(input_lines):

    def first_line(been, point, steps_counter):
        if not point in been:
            been[point] = (False, steps_counter, 0)

    def second_line(been, point, steps_counter):
        if point in been:
            _, first_line_steps, second_line_steps = been[point]
            been[point] = (True, first_line_steps, steps_counter if second_line_steps == 0 else second_line_steps)

    been = position_the_line(input_lines[0], {}, first_line)
    position_the_line(input_lines[1], been, second_line)

    return min([v[1] + v[2] for k, v in been.items() if v[0] == True])


assert solution_for_second_part('''R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83'''.splitlines()) == 610

assert solution_for_second_part('''R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'''.splitlines()) == 410

print("Solution for the second part:", solution_for_second_part(input_lines))
