def load_input_file(file_name: str) -> [str]:
    with open(file_name) as file:
        yield from (int(line.strip()) for line in file)


def find_increased(measurements):
    return sum(1 for previous, current in zip(measurements[1:], measurements) if previous > current)


def solution_for_first_part(input):
    return find_increased(input)


example_input = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
assert solution_for_first_part(example_input) == 7

# The input is taken from: https://adventofcode.com/2021/day/1/input
task_input = list(load_input_file('input.01.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(measurements):
    windows = [a + b + c for a, b, c in zip(measurements, measurements[1:], measurements[2:])]

    return find_increased(windows)


assert solution_for_second_part(example_input) == 5
print("Solution for the second part:", solution_for_second_part(task_input))
