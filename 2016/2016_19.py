import math


def load_input_file(file_name):
    with open(file_name) as file:
        return int(file.read().strip())


def numer_elves_with_all_presents(elves_number: int) -> int:
    last_2_power = math.floor(math.log(elves_number, 2))

    return (elves_number - 2 ** last_2_power) * 2 + 1

# The input is taken from: https://adventofcode.com/2016/day/19/input
elves_number = load_input_file('input.19.txt')
print("Solution for the first part:", numer_elves_with_all_presents(elves_number))
