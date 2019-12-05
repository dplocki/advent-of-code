import math


def load_input_file(file_name):
    with open(file_name) as file:
        return int(file.read().strip())


def solution_for_first_part(elves_number: int) -> int:
    last_2_power = math.floor(math.log(elves_number, 2))

    return (elves_number - 2 ** last_2_power) * 2 + 1


# The input is taken from: https://adventofcode.com/2016/day/19/input
elves_number = load_input_file('input.19.txt')
print("Solution for the first part:", solution_for_first_part(elves_number))


def solution_for_second_part(elves_number: int) -> int:
    power_3_last = 3 ** math.floor(math.log(elves_number - 1, 3))

    if elves_number <= power_3_last * 2:
        return elves_number - power_3_last
    else:
        return 2 * elves_number - 3 * power_3_last


print("Solution for the second part:", solution_for_second_part(elves_number))
