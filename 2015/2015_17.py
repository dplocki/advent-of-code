import itertools


WANTED_SIZE = 150


def load_input_file(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def wanted_storativity_containers_combinations_generator(containers: list):
    containers_number = len(containers)

    for combination in itertools.product([True, False], repeat=containers_number):
        storativity = sum(containers[index] for index in range(containers_number) if combination[index])
        if storativity == WANTED_SIZE:
            yield combination


def solution_for_second_part(combinations):
    containers_in_combinations = [sum(1 for c in combination if c) for combination in combinations]
    minimum_number = min(containers_in_combinations)

    return sum(1 for c in containers_in_combinations if c == minimum_number)


# The input is taken from: https://adventofcode.com/2015/day/17/input
containers = list(map(int, load_input_file('input.17.txt')))
all_combinations = list(wanted_storativity_containers_combinations_generator(containers))

print("Solution for the first part:", len(all_combinations))
print("Solution for the second part:", solution_for_second_part(all_combinations))
