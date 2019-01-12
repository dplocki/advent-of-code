GRID_SIZE = 300
TESTING = False


def cell_power(x: int, y: int, grid_serial_number: int):
    rack_id = x + 10
    power_level = (rack_id * y + grid_serial_number) * rack_id

    return int(power_level / 100) % 10 - 5


def build_grid(grid_serial_number: int):

    def build_cell_power_grid(grid_serial_number):
        return {
            (x,y):cell_power(x, y, grid_serial_number)
            for y in range(GRID_SIZE)
            for x in range(GRID_SIZE)
        }

    grid = build_cell_power_grid(grid_serial_number)

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            grid[(x,y)] = grid[(x,y)] + grid.get((x, y - 1), 0) + grid.get((x - 1, y), 0) - grid.get((x - 1, y - 1), 0)

    return grid


def grid_sum_for_size(sum_table: [int], size = 3):
    def calculate_sum(x, y, size):
        return sum_table[(x + size - 1, y + size - 1)] \
            + sum_table.get((x - 1, y - 1), 0) \
            - sum_table.get((x - 1, y + size - 1), 0) \
            - sum_table.get((x + size - 1, y - 1), 0)

    return {
        (x, y): calculate_sum(x, y, size)
        for y in range(0, GRID_SIZE - size)
        for x in range(0, GRID_SIZE - size)
    }


def find_maximum_for_size(grid: {tuple:int}, size = 3):
    power_level_grid = grid_sum_for_size(grid, size)
    maximum = max(power_level_grid, key=power_level_grid.get)
    return maximum, power_level_grid[maximum]


def find_coordinate_of_the_biggest_for_size(grid: {tuple:int}):
    return find_maximum_for_size(grid, 3)[0]


def find_the_coordinate_and_the_sum_grid_size(grid: {tuple:int}):
    results = {size:find_maximum_for_size(grid, size) for size in range(1, 300)}
    best_size = max(results, key=lambda x:results[x][1])

    return results[best_size][0], best_size


if TESTING:

    assert cell_power(3, 5, 8) == 4
    assert cell_power(122, 79, 57) == -5
    assert cell_power(217, 196, 39) == 0
    assert cell_power(101, 153, 71) == 4

    test_18_grid = build_grid(18)
    test_42_grid = build_grid(42)

    assert find_coordinate_of_the_biggest_for_size(test_18_grid) == (33, 45)
    assert find_coordinate_of_the_biggest_for_size(test_42_grid) == (21, 61)

    assert find_the_coordinate_and_the_sum_grid_size(test_18_grid) == ((90, 269), 16)
    assert find_the_coordinate_and_the_sum_grid_size(test_42_grid) == ((232, 251), 12)

else:

    task_grid = build_grid(8561)

    first_part_solution = find_coordinate_of_the_biggest_for_size(task_grid)
    print(f"Solution for first part: {first_part_solution[0]},{first_part_solution[1]}")

    maximum_point, size = find_the_coordinate_and_the_sum_grid_size(task_grid)
    print(f"Solution for second part: {maximum_point[0]},{maximum_point[1]},{size}")
