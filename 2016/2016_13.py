def load_input_file(file_name):
    with open(file_name) as file:
        return int(file.read())


def is_open(x: int, y: int, favorite: int) -> bool:
    return format(x*x + 3*x + 2*x*y + y + y*y + favorite, 'b').count('1') % 2 == 0


def find_fastest_path(favorite, where):

    def get_posibilities(where):
        tmp = [
                (where[0] - 1, where[1]),
                (where[0] + 1, where[1]),
                (where[0], where[1] - 1),
                (where[0], where[1] + 1)
            ]

        for t in tmp:
            if is_open(t[0], t[1], favorite):
                if t[0] > 0 and t[0] > 0:
                    yield t


    been = set()
    posibilities = [(0, (1, 1))]
    while posibilities:
        steps_number, point = posibilities.pop(0)

        if point == where:
            return steps_number

        print(list(get_posibilities(point)))
        for next in get_posibilities(point):
            if next in been:
                continue

            been.add(next)
            posibilities.append((steps_number + 1, next))


assert find_fastest_path(10, (7,4)) == 11

# The input is taken from: https://adventofcode.com/2016/day/13/input
favorite = load_input_file('input.13.txt')
print("Solution for the first part:", find_fastest_path(favorite, (31,39)))
