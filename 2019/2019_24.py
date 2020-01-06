from collections import defaultdict


GRID_SIZE = 5
GRID_CENTER = 2


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
        return sum(1 if grid.get(neighbor, False) else 0 for neighbor in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])


    def bug_will_died(grid: dict, x: int, y: int) -> bool:
        return count_neighbor_bugs(grid, x, y) == 1


    def bug_will_born(grid: dict, x: int, y: int) -> bool:
        return 0 < count_neighbor_bugs(grid, x, y) < 3


    def calculate_biodiversity_rating(grid: dict) -> int:
        return sum(i * power for i, power in zip([
            1 if grid[x, y] else 0
            for y in range(GRID_SIZE)
            for x in range(GRID_SIZE)
        ], power_two_generator()))

    
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


def solution_for_first_part(grid: dict):
    been = set()

    for state in bugs_generator(grid):
        if state in been:
            return state

        been.add(state)


assert solution_for_first_part(parse('''....#
#..#.
#..##
..#..
#....'''.splitlines())) == 2129920


# The input is taken from: https://adventofcode.com/2019/day/24/input
grid = parse(load_input_file('input.24.txt'))
print("Solution for the first part:", solution_for_first_part(grid))


def bugs_multidemention_generator(grid: dict):

    def bugs_on_single_level(grids: dict, level: int) -> dict:
        result = {}

        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if x == GRID_CENTER and y == GRID_CENTER:
                    continue
                
                base = sum(
                        1 if grids[level].get(neighbor, False) else 0
                        for neighbor in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
                    )

                if x == 0:
                    base += grids[level - 1].get((1, GRID_CENTER), False)
                
                if x == GRID_SIZE - 1:
                    base += grids[level - 1].get((3, GRID_CENTER), False)

                if y == 0:
                    base += grids[level - 1].get((GRID_CENTER, 1), False)

                if y == GRID_SIZE - 1:
                    base += grids[level - 1].get((GRID_CENTER, 3), False)

                if x == 1 and y == 2:
                    base += sum(1 for i in range(GRID_SIZE) if grids[level + 1].get((0, i), False))

                if x == 2 and y == 1:
                    base += sum(1 for i in range(GRID_SIZE) if grids[level + 1].get((i, 0), False))

                if x == 3 and y == 2:
                    base += sum(1 for i in range(GRID_SIZE) if grids[level + 1].get((4, i), False))

                if x == 2 and y == 3:
                    base += sum(1 for i in range(GRID_SIZE) if grids[level + 1].get((i, 4), False))

                result[x, y] = base == 1 if grids[level].get((x, y), False) else base == 2 or base == 1

        return result


    grids = defaultdict(dict)
    grids[0] = grid

    while True:
        levels = sorted(grids.keys())

        new_grids = defaultdict(dict)
        for level in levels + [min(levels) - 1, max(levels) + 1]:
            temp = bugs_on_single_level(grids, level)
            if any(temp.keys()):
                new_grids[level] = temp

        grids = new_grids
        yield grids


def bugs_after_time(grid, minutes):
    for _, state in zip(range(minutes), bugs_multidemention_generator(grid)):
        pass

    return sum(list(grid.values()).count(True) for level, grid in state.items())


def solution_for_second_part(grid: dict) -> int:
    return bugs_after_time(grid, 200)


assert bugs_after_time(parse('''....#
#..#.
#.?##
..#..
#....'''.splitlines()), 10) == 99


print("Solution for the second part:", solution_for_second_part(grid))
