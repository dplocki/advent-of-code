from array import array


GRID_SIZE = 300


def cell_power(x: int, y: int, grid_serial_number: int):
    rack_id = x + 10
    power_level = (rack_id * y + grid_serial_number) * rack_id

    return int(power_level / 100) % 10 - 5


def build_grid(grid_serial_number: int):
    return [cell_power(x, y, grid_serial_number) for y in range(GRID_SIZE) for x in range(GRID_SIZE)]


def grid_sum_for_size(grid: [int], size = 3):
    return [
        sum([grid[GRID_SIZE*(y + iy) + (x + ix)] for iy in range(size) for ix in range(size)])
        for x in range(0, GRID_SIZE - size)
        for y in range(0, GRID_SIZE - size)
    ]


def grid_to_string(grid: [int], size = GRID_SIZE) -> str:
    result = ''
    for y in range(size):
        for x in range(size):
            tmp = grid[size*y + x]
            result += str(tmp).zfill(3)
            result += ' '
        result += '\n'

    return result


def index_to_2d_coordinates(index: int, grid_size: int):
    return  (index % grid_size), int(index / grid_size)


def find_coordinate_of_the_biggest_for_size(grid: [int], size = 3):
    grid_size = GRID_SIZE - size
    power_level_grid = grid_sum_for_size(grid, size)

    maximum = max(power_level_grid)
    index_of_maxium = power_level_grid.index(maximum)

    return index_to_2d_coordinates(index_of_maxium, grid_size)


assert cell_power(3, 5, 8) == 4
assert cell_power(122, 79, 57) == -5
assert cell_power(217, 196, 39) == 0
assert cell_power(101, 153, 71) == 4

test_18_grid = build_grid(18)
test_42_grid = build_grid(42)
assert len(grid_sum_for_size(test_18_grid, 3)) == 297 ** 2

assert index_to_2d_coordinates(23 * GRID_SIZE + 2, GRID_SIZE) == (2, 23)
assert index_to_2d_coordinates(45 * GRID_SIZE + 12, GRID_SIZE) == (12, 45)

assert find_coordinate_of_the_biggest_for_size(test_18_grid) == (45, 33)
assert find_coordinate_of_the_biggest_for_size(test_42_grid) == (61, 21)

first_part_solution = find_coordinate_of_the_biggest_for_size(build_grid(8561))
print(f"Solution for first part: {first_part_solution[1]},{first_part_solution[0]}")


def increase_sum_grid(original_grid: [int],
                      actual_grid: [int],
                      actual_sum_square_size: int,
                      grid_size: int = GRID_SIZE):
    working_grid_size = grid_size - actual_sum_square_size
    maximum = 0
    maximum_position = None

    for x in range(working_grid_size):
        for y in range(working_grid_size):
            new_value = actual_grid[grid_size * y + x] \
            + sum([original_grid[grid_size * (y + actual_sum_square_size) + x + i] for i in range(actual_sum_square_size)]) \
            + sum([original_grid[grid_size * (y + i) + (x + actual_sum_square_size)] for i in range(actual_sum_square_size)]) \
            + original_grid[grid_size * (y + actual_sum_square_size) + x + actual_sum_square_size]

            if new_value > maximum:
                maximum = new_value
                maximum_position = (x, y)
                

            actual_grid[grid_size * y + x] = new_value

    return maximum, maximum_position, actual_grid

test = [
    1,2,
    3,4]

assert increase_sum_grid(test, test[:], 1, 2) == (10, (0, 0), [10, 2, 3, 4])

test = [
    1, 2, 3,
    4, 5, 6,
    7, 8, 9]

assert increase_sum_grid(test, test[:], 1, 3) == (28, (1, 1), [
    12, 16, 3,
    24, 28, 6,
    7, 8, 9])

test = [
    1, 0, 2,
    0, 0, 3,
    4, 5, 6]

assert increase_sum_grid(test, test[:], 1, 3) == (14, (1, 1), [
    1, 5, 2,
    9, 14, 3,
    4, 5, 6])

test = [
    1, 0, 2,
    0, 0, 3,
    4, 5, 6]

assert increase_sum_grid(test, test[:], 2, 3) == (21, (0, 0), [
    21, 0, 2,
    0, 0, 3,
    4, 5, 6])

test = [
    0, 0, 0, 1,
    0, 0, 0, 1,
    0, 0, 0, 1,
    0, 0, 0, 1]

assert increase_sum_grid(test, test[:], 2, 4) == (3, (1, 0), [
    0, 3, 0, 1,
    0, 3, 0, 1,
    0, 0, 0, 1,
    0, 0, 0, 1])

test = [
    0, 0, 0, 1,
    0, 0, 0, 1,
    0, 0, 0, 1,
    1, 1, 1, 1]

assert increase_sum_grid(test, test[:], 2, 4) == (5, (1, 1), [
    0, 3, 0, 1,
    3, 5, 0, 1,
    0, 0, 0, 1,
    1, 1, 1, 1])

test = [
    1, 1, 1, 1,
    1, 1, 1, 1,
    1, 1, 1, 1,
    1, 1, 1, 1]

assert increase_sum_grid(test, test[:], 1, 4) == (4, (0, 0), [
    4, 4, 4, 1,
    4, 4, 4, 1,
    4, 4, 4, 1,
    1, 1, 1, 1])


def find_the_coordinate_and_the_sum_grid_size(entry_grid):
    maximum = 0
    maximum_point = None
    maximum_size = None
    actual_gird = array('i', entry_grid)

    for size in range(1, 300):
        local_maximum, local_maximum_position, actual_gird = increase_sum_grid(entry_grid, actual_gird, size)

        if local_maximum > maximum:
            maximum = local_maximum
            maximum_point = local_maximum_position
            maximum_size = size + 1

    return maximum_point, maximum_size


test_18_grid = build_grid(18)
assert find_the_coordinate_and_the_sum_grid_size(test_18_grid) == ((90, 269), 16)

maximum_point, size = find_the_coordinate_and_the_sum_grid_size(build_grid(8561))
print(f"Solution for second part: {maximum_point[0]},{maximum_point[1]},{size}")
