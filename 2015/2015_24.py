from functools import reduce
import sys


def load_input_file(file_name):
    with open(file_name) as file:
        yield from (int(line.strip()) for line in file)


def solution_for_first_part(input: [int]):

    def subset_sum(numbers, target, partial=[]):
        sum_of_current = sum(partial)

        # check if the partial sum is equals to target
        if sum_of_current == target:
            yield partial

        if sum_of_current >= target:
            return  # if we reach the number why bother to continue

        for index, number in enumerate(numbers):
            yield from subset_sum(numbers[index + 1:], target, partial + [number]) 


    all_packages_list = list(input)
    single_group_size = sum(all_packages_list) // 3

    all_combination_for_first_group = list(subset_sum(all_packages_list, single_group_size))

    min_first_group_length = reduce(lambda x, y: min(x, len(y)), all_combination_for_first_group, sys.maxsize)
    all_lowest_first_group_combinations = filter(lambda x: len(x) == min_first_group_length, all_combination_for_first_group)
    group_combinations_with_entanglement = map(lambda x: (x, reduce(lambda r, l: r * l, x, 1)), all_lowest_first_group_combinations)
    sorted_first_group_combinations = sorted(group_combinations_with_entanglement, key=lambda x: x[1])

    return sorted_first_group_combinations[0][1]


print("Solution for the first part:", solution_for_first_part(load_input_file('input.24.txt')))
