from functools import reduce
import sys


def load_input_file(file_name):
    with open(file_name) as file:
        yield from (int(line.strip()) for line in file)


def solution(all_packages_list: [int], how_many_groups):

    def subset_sum(numbers, target, partial=[]):
        sum_of_current = sum(partial)

        if sum_of_current == target:
            yield partial

        if sum_of_current >= target:
            return

        for index, number in enumerate(numbers):
            yield from subset_sum(numbers[index + 1:], target, partial + [number]) 

    single_group_size = sum(all_packages_list) // how_many_groups
    all_combination_for_first_group = list(subset_sum(all_packages_list, single_group_size))

    min_first_group_length = reduce(lambda x, y: min(x, len(y)), all_combination_for_first_group, sys.maxsize)
    all_lowest_first_group_combinations = filter(lambda x: len(x) == min_first_group_length, all_combination_for_first_group)
    group_combinations_with_entanglement = map(lambda x: (x, reduce(lambda r, l: r * l, x, 1)), all_lowest_first_group_combinations)
    sorted_first_group_combinations = sorted(group_combinations_with_entanglement, key=lambda x: x[1])

    return sorted_first_group_combinations[0][1]


# The input is taken from: https://adventofcode.com/2015/day/24/input
input_list = list(load_input_file('input.24.txt'))
print("Solution for the first part:", solution(input_list, 3))
print("Solution for the second part:", solution(input_list, 4))
