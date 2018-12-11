GRID_SIZE = 300


def cell_power(x: int, y: int, grid_serial_number: int):
    rack_id = x + 10
    power_level = (rack_id * y + grid_serial_number) * rack_id

    return int(power_level / 100) % 10 - 5


assert cell_power(3, 5, 8) == 4
assert cell_power(122, 79, 57) == -5
assert cell_power(217, 196, 39) == 0
assert cell_power(101, 153, 71) == 4


def build_grid(grid_serial_number: int):
    return [cell_power(x, y, grid_serial_number) for y in range(GRID_SIZE) for x in range(GRID_SIZE)]


def grid_sum_3x3(grid: [int]):
    return [
        sum([grid[GRID_SIZE*(y + iy) + (x + ix)] for iy in [0, 1, 2] for ix in [0, 1, 2]])
        for x in range(0, GRID_SIZE - 2)
        for y in range(1, GRID_SIZE - 2)
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


def find_coordinate_of_the_biggest(grid: [int]):
    grid_size = GRID_SIZE - 3
    power_level_grid = grid_sum_3x3(grid)

    maximum = max(power_level_grid)
    index_of_maxium = power_level_grid.index(maximum)

    return int(index_of_maxium / grid_size), (index_of_maxium % grid_size) + 1


assert find_coordinate_of_the_biggest(build_grid(18)) == (33, 45)
assert find_coordinate_of_the_biggest(build_grid(42)) == (21, 61)

print("Solution for first part:", find_coordinate_of_the_biggest(build_grid(8561)))
