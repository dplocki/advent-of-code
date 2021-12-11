MINIMUM_ENERGY_LEVEL = 0
FLASH_ENERGY_LEVEL = 10


def load_input_file(file_name: str) -> list[str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: list[str]) -> list[tuple[int, int, int]]:
    for row, line in enumerate(task_input):
        for column, character in enumerate(line):
            yield column, row, int(character)


def get_eight_neighbors(x: int, y: int) -> list[tuple[int, int]]:
    yield (x, y - 1)     # N
    yield (x + 1, y - 1) # NE
    yield (x + 1, y)     # E
    yield (x + 1, y + 1) # SE
    yield (x, y + 1)     # S
    yield (x - 1, y + 1) # SW
    yield (x - 1, y)     # W
    yield (x - 1, y - 1) # NW


def octopuses_similator(task_input: list[tuple[int, int, int]]) -> int:
    octopuses = {(column, row):energy_level for column, row, energy_level in parse(task_input)}
  
    while True:
        octopuses = {position:(energy_level + 1) for position, energy_level in octopuses.items()}

        flashing = [position for position, value in octopuses.items() if value == FLASH_ENERGY_LEVEL]
        while flashing:
            current_flashing_position = flashing.pop()

            for neighbore in get_eight_neighbors(*current_flashing_position):
                if neighbore not in octopuses:
                    continue

                octopuses[neighbore] = octopuses[neighbore] + 1
                if octopuses[neighbore] == FLASH_ENERGY_LEVEL:
                    flashing.append(neighbore)

        octopuses = {position:(energy_level if energy_level < FLASH_ENERGY_LEVEL else MINIMUM_ENERGY_LEVEL) for position, energy_level in octopuses.items()}
        yield octopuses


def solution_for_first_part(task_input: list[tuple[int, int, int]]) -> int:
    flashes = 0
    for octopuses, _ in zip(octopuses_similator(task_input), range(100)):
        flashes += sum(1 for energy_level in octopuses.values() if energy_level == MINIMUM_ENERGY_LEVEL)

    return flashes


example_input = '''5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526'''.splitlines()

assert solution_for_first_part(example_input) == 1656

# The input is taken from: https://adventofcode.com/2021/day/11/input
task_input = list(load_input_file('input.11.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: list[tuple[int, int, int]]) -> int:
    zero_filter = lambda energy_level: energy_level == 0
    step = 0
    for octopuses in octopuses_similator(task_input):
        step += 1
        if all(map(zero_filter, octopuses.values())):
            return step


assert solution_for_second_part(example_input) == 195
print("Solution for the second part:", solution_for_second_part(task_input))
