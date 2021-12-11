FLASH_ENERGY_LEVEL = 10


def load_input_file(file_name: str) -> list[str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: list[str]):
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


def solution_for_first_part(task_input: list[tuple[int, int, int]]):
    octopuses = {(column, row):energy_level for column, row, energy_level in parse(task_input)}
  
    flashes = 0
    for _ in range(100):
        octopuses = {position:(energy_level + 1) for position, energy_level in octopuses.items()}
        
        flashing = [position for position, value in octopuses.items() if value == FLASH_ENERGY_LEVEL]
        flashes += len(flashing)

        while flashing:
            current_flashing_position = flashing.pop()

            for neighbore in get_eight_neighbors(*current_flashing_position):
                if neighbore in octopuses:
                    octopuses[neighbore] = octopuses[neighbore] + 1
                    if octopuses[neighbore] == FLASH_ENERGY_LEVEL:
                        flashes += 1
                        flashing.append(neighbore)

        octopuses = {position:(energy_level if energy_level < FLASH_ENERGY_LEVEL else 0) for position, energy_level in octopuses.items()}

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
