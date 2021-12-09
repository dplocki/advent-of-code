MAXIUM_HEIGHT = 9


def load_input_file(file_name: str) -> list[str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: list[str]):
    for row_number, line in enumerate(task_input):
        for column_number, digit in enumerate(line):
            yield row_number, column_number, int(digit)


def get_four_neighbors(x, y):
    yield (x, y - 1) # NORTH
    yield (x + 1, y) # EAST
    yield (x, y + 1) # SOUTH
    yield (x - 1, y) # WEST


def solution_for_first_part(task_input):
    height_map = {(row, column):value for row, column, value in parse(task_input)}

    return sum(
        height + 1
        for coordinate, height in height_map.items()
        if all(map(lambda neighbore: height_map.get(neighbore, MAXIUM_HEIGHT) > height, get_four_neighbors(*coordinate))))


example_input = '''2199943210
3987894921
9856789892
8767896789
9899965678'''.splitlines()

assert solution_for_first_part(example_input) == 15

# The input is taken from: https://adventofcode.com/2021/day/9/input
task_input = list(load_input_file('input.09.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
