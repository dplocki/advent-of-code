def load_input_file(file_name: str) -> list[str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: list[str]) -> list[tuple[int, int, str]]:
    for row, line in enumerate(task_input):
        for column, character in enumerate(line):
            yield column, row, character


def solution_for_first_part(task_input: list[str]) -> int:
    raw_map = list(parse(task_input))
    easts = {(x, y) for x, y, value in raw_map if value == '>'}
    souths = {(x, y) for x, y, value in raw_map if value == 'v'}

    max_x = max(x for x, _, _ in raw_map) + 1
    max_y = max(y for _, y, _ in raw_map) + 1

    step = 0
    while True:
        step += 1

        new_easts = set()
        for cucumber in easts:
            new_position = ((cucumber[0] + 1) % max_x, cucumber[1])

            if new_position in easts or new_position in souths:
                new_easts.add(cucumber)
            else:
                new_easts.add(new_position)

        new_souths = set()
        for cucumber in souths:
            new_position = (cucumber[0], (cucumber[1] + 1) % max_y)
            if new_position in new_easts or new_position in souths:
                new_souths.add(cucumber)
            else:
                new_souths.add(new_position)

        if souths == new_souths and easts == new_easts:
            return step

        souths = new_souths
        easts = new_easts


example_input = '''v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>'''.splitlines()

assert solution_for_first_part(example_input) == 58

# The input is taken from: https://adventofcode.com/2021/day/25/input
task_input = list(load_input_file('input.25.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))