from typing import Generator, Iterable, Set, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def validation_direction() -> Generator[Tuple[Tuple[int, int], ...], None, None]:
    while True:
        yield (-1, -1), (-1, 0), (-1, 1)
        yield (1, -1), (1, 0), (1, 1)
        yield (-1, -1), (0, -1), (1, -1)
        yield (-1, 1), (0, 1), (1, 1)


def all_neighbors(row_index: int, column_index: int) -> Generator[Tuple[int, int], None, None]:
    directions = ((-1, -1), (0, -1), (1, -1), (-1, 0),  (1, 0), (-1, 1), (0, 1), (1, 1))

    yield from (
        (row_index + y, column_index + x)
        for y, x in directions)


def parse(task_input: Iterable[str]) -> Set[Tuple[int, int]]:
    return set(
            (row_index, column_index)
            for row_index, line in enumerate(task_input)
            for column_index, c in enumerate(line)
            if c == '#')


def solution_for_first_part(task_input: Iterable[str]) -> int:
    current_elves = parse(task_input)
    validation_direction_generator = validation_direction()
    will_be_occupied = {} # where elf will be moved -> where elf is now

    for _ in range(10):
        new_elves = set()
        directions = [d for d, _ in zip(validation_direction_generator, range(4))]

        for elf_position in current_elves:
            new_elves.add(elf_position)

            if not current_elves & set(all_neighbors(*elf_position)):
                continue

            for direction in directions:
                if current_elves & set((elf_position[0] + y, elf_position[1] + x) for y, x in direction):
                    continue

                new_place = elf_position[0] + direction[1][0], elf_position[1] + direction[1][1]

                if new_place in new_elves:
                    new_elves.remove(new_place)
                    new_elves.add(will_be_occupied[new_place])
                    new_elves.add(elf_position)
                else:
                    new_elves.remove(elf_position)
                    new_elves.add(new_place)
                    will_be_occupied[new_place] = elf_position

                break

        current_elves = new_elves            

    xs = [x for _, x in current_elves]
    ys = [y for y, _ in current_elves]
    max_x = max(xs)
    max_y = max(ys)
    min_x = min(xs)
    min_y = min(ys)
    
    return (abs(max_x - min_x) + 1) * (abs(max_y - min_y) + 1) - len(current_elves)


example_input = '''....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..'''.splitlines()

assert solution_for_first_part(example_input) == 110
# The input is taken from: https://adventofcode.com/2022/day/23/input
task_input = list(load_input_file('input.23.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
