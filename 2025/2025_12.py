from typing import Dict, Iterable, List, Set, Tuple


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def parse(task_input: Iterable[str]) -> Tuple[Dict[int, Set], List[Tuple[Tuple[int, int], Tuple[int, ...]]]]:

    def parse_present(token: str) -> Tuple[int, str]:
        lines = token.splitlines()

        index = int(lines[0][:-1])
        present = set(
            (ri, rc)
            for ri, line in enumerate(lines[1:])
            for rc, character in enumerate(line)
            if character == '#')

        return index, present


    def parse_region(line: str) -> Tuple[Tuple[int, int], Tuple[int, ...]]:
        region_size, presents_list = line.split(': ')
        rows, columns = map(int, region_size.split('x'))

        return (rows, columns), tuple(map(int, presents_list.split(' ')))


    tokens = task_input.split('\n\n')

    presents = {
        index: present
        for index, present in map(parse_present, tokens[:-1])
    }

    regions = list(map(parse_region, tokens[-1].splitlines()))

    return presents, regions


def can_all_presents_be_fit(area: Tuple[int, ...]) -> bool:
    (size_r, size_c), how_much = area

    return (size_r // 3) * (size_c // 3) >= sum(how_much)


def solution_for_first_part(task_input: Iterable[str]) -> int:
    _, regions = parse(task_input)

    return sum(1
        for region in regions
        if can_all_presents_be_fit(region)
    )


example_input = '''0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
'''

# The input is taken from: https://adventofcode.com/2025/day/12/input
task_input = load_input_file('input.12.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
