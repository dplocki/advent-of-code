STARTING_POINT = (1, 1)


def load_input_file(file_name):
    with open(file_name) as file:
        return int(file.read())


def is_open(x: int, y: int, favorite: int) -> bool:
    return format(x*x + 3*x + 2*x*y + y + y*y + favorite, 'b').count('1') % 2 == 0


def get_possibilities(favorite: int, where: tuple) -> int:
    tmp = [
            (where[0] - 1, where[1]),
            (where[0] + 1, where[1]),
            (where[0], where[1] - 1),
            (where[0], where[1] + 1)
        ]

    yield from [t for t in tmp if t[0] >= 0 and t[1] >= 0 and is_open(t[0], t[1], favorite)]


def find_fastest_path(favorite: int, where: int) -> int:
    been = set()
    possibilities = [(0, STARTING_POINT)]
    while possibilities:
        steps_number, point = possibilities.pop(0)

        if point == where:
            return steps_number

        for next in get_possibilities(favorite, point):
            if next in been:
                continue

            been.add(next)
            possibilities.append((steps_number + 1, next))


assert find_fastest_path(10, (7,4)) == 11

# The input is taken from: https://adventofcode.com/2016/day/13/input
favorite = load_input_file('input.13.txt')
print("Solution for the first part:", find_fastest_path(favorite, (31,39)))


def count_positions_in_reach(favorite: int, max_steps: int) -> int:
    been = {STARTING_POINT: 0}
    possibilities = [(0, STARTING_POINT)]
    while possibilities:
        steps_number, point = possibilities.pop(0)

        if steps_number > max_steps:
            continue

        for next in get_possibilities(favorite, point):
            new_steps_value = steps_number + 1
            if next in been:
                been[next] = new_steps_value if been[next] > new_steps_value else been[next]
                continue

            been[next] = new_steps_value
            possibilities.append((new_steps_value, next))

    return len([k for k, v in been.items() if v <= max_steps])


print("Solution for the second part:", count_positions_in_reach(favorite, 50))
