from typing import Dict, Generator, Iterable, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Dict[Tuple[int, int], str]:
    return {(row, column): character
            for row, line in enumerate(task_input)
            for column, character in enumerate(line)
            if character in 'O#'}


def count_total_load(rock_map: Dict[Tuple[int, int], str], maximum_rows: int) -> int:
    return sum(
        maximum_rows - position[0] + 1
        for position, object in rock_map.items()
        if object == 'O')


def solution_for_first_part(task_input: Iterable[str]) -> int:
    rock_map = parse(task_input)

    rs = [r for r, c in rock_map.keys()]
    cs = [c for r, c in rock_map.keys()]
    maximum_row = max(rs)
    maximum_column = max(cs)

    new_rock_map = {}
    for column_index in range(0, maximum_column + 1):
        column = {k[0]:v for k,v in rock_map.items() if column_index == k[1]}

        for c in column:
            if column[c] == 'O':
                rocks_before = {i:column[i] for i in range(c) if i in column and column[i] == '#'}
                if len(rocks_before) == 0:
                    new_rock_map[sum(1 for i in range(c) if i in column and column[i] == 'O'), column_index] = 'O'
                else:
                    top = max(rocks_before.keys())
                    new_rock_map[top + 1 + sum(1 for i in range(top, c) if i in column and column[i] == 'O'), column_index] = 'O'

    return count_total_load(new_rock_map, maximum_row)


example_input = '''O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....'''.splitlines()

assert solution_for_first_part(example_input) == 136

# The input is taken from: https://adventofcode.com/2023/day/14/input
task_input = list(load_input_file('input.14.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
