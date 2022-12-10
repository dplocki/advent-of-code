from typing import Generator, Iterable, Tuple, Union


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[str, Union[int, None]], None, None]:
    for line in task_input:
        tokens = line.split(' ')
        yield tokens[0], int(tokens[1]) if len(tokens) > 1 else None


def run_program(instructions) -> Generator[Tuple[int, int], None, None]:
    x = 1
    cycle = 1

    for instruction, value in instructions:
        if instruction == 'noop':
            yield cycle, x
            cycle += 1
        elif instruction == 'addx':
            yield cycle, x
            cycle += 1
            yield cycle, x
            cycle += 1
            x += value


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return sum(
        x_value * cycle
        for cycle, x_value in run_program(parse(task_input))
        if ((cycle - 20) % 40) == 0)


example_input = '''addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop'''.splitlines()

assert solution_for_first_part(example_input) == 13140

# The input is taken from: https://adventofcode.com/2022/day/10/input
task_input = list(load_input_file('input.10.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> None:
    SCREEN_WIDTH = 40
    SCREEN_HEIGHT = 6

    screen = {}
    for cycle, x_value in run_program(parse(task_input)):
        column = (cycle - 1) % SCREEN_WIDTH
        row = (cycle - 1) // SCREEN_WIDTH

        screen[column, row] = '#' if abs(x_value - column) <= 1 else '.'

    for row in range(SCREEN_HEIGHT):
        for column in range(SCREEN_WIDTH):
            print(screen[column, row], end='')

        print()


print("Solution for the second part:")
solution_for_second_part(task_input)
