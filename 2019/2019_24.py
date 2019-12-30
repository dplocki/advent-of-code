GRID_SIZE = 5


def load_input_file(file_name: str):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(input: list):
    result = {}

    for y, line in enumerate(input):
        for x, c in enumerate(line):
            result[(x, y)] = (c == '#')

    return result


def bugs_generator(grid: dict):

    def power_two_generator():
        n = 1
        while True:
            yield n
            n *= 2    


    def count_neighbor_bugs(grid: dict, x: int, y: int) -> int:
        return sum([1 if grid.get(neighbor, False) else 0 for neighbor in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]])


    def bug_will_died(grid: dict, x: int, y: int) -> bool:
        return count_neighbor_bugs(grid, x, y) == 1


    def bug_will_born(grid: dict, x: int, y: int) -> bool:
        return 0 < count_neighbor_bugs(grid, x, y) < 3


    def calculate_biodiversity_rating(grid: dict) -> int:
        return sum([i * power for i, power in zip([
            1 if grid[x, y] else 0
            for y in range(GRID_SIZE)
            for x in range(GRID_SIZE)
        ], power_two_generator())])

    
    def build_new_grid(grid: dict) -> dict:
        return {
                (x, y): bug_will_died(grid, x, y) if grid[x, y] else bug_will_born(grid, x, y)
                for x in range(GRID_SIZE)
                for y in range(GRID_SIZE)
            }


    while True:
        new_grid = build_new_grid(grid)
        yield calculate_biodiversity_rating(new_grid)
        grid = new_grid


def solution_for_first_part(task_input: str):
    grids = parse(task_input)
    been = set()

    for state in bugs_generator(grids):
        if state in been:
            return state

        been.add(state)


assert solution_for_first_part('''....#
#..#.
#..##
..#..
#....'''.splitlines()) == 2129920


# The input is taken from: https://adventofcode.com/2019/day/24/input
task_input = load_input_file('input.24.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


