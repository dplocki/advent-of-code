from typing import Generator, Iterable, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple, None, None]:
    for line in task_input:
        yield tuple(map(int, line))


def the_highest_joltage(batteries: Tuple[int, ...], max_digits: int) -> int:
    result = 0
    start = 0
    len_batteries = len(batteries)

    for place_left in range(max_digits, 0, -1):
        max_index = start
        max_value = batteries[max_index]

        for index in range(start + 1, len_batteries - place_left + 1):
            if batteries[index] > max_value:
                max_value = batteries[index]
                max_index = index

            if max_value == 9:
                break

        digit = batteries[max_index]
        start = max_index + 1
        result = result * 10 + digit

    return result


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return sum(
        the_highest_joltage(batteries, 2)
        for batteries in parse(task_input)
    )


example_input = '''987654321111111
811111111111119
234234234234278
818181911112111'''.splitlines()

assert solution_for_first_part(example_input) == 357

# The input is taken from: https://adventofcode.com/2025/day/3/input
task_input = list(load_input_file('input.03.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> int:
    return sum(
        the_highest_joltage(batteries, 12)
        for batteries in parse(task_input)
    )


assert solution_for_second_part(example_input) == 3121910778619
print("Solution for the second part:", solution_for_second_part(task_input))
