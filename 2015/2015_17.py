import itertools


WANTED_SIZE = 150


def load_input_file(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def containers_combinations_generator(containers: list):
    containers_number = len(containers)

    yield from (
            sum(
                containers[index]
                for index in range(containers_number)
                if product[index]
            )
            for product in itertools.product([True, False],  repeat=containers_number)
        )


def solution_for_first_part(containers):
    return sum(
            1
            for storativity in containers_combinations_generator(containers)
            if storativity == WANTED_SIZE
        )


# The solution is taken from: https://adventofcode.com/2015/day/17/input
containers = list(map(int, load_input_file('input.17.txt')))
print("Solution for the first part:", solution_for_first_part(containers))
