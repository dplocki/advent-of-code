import re
import functools
import operator


TRAITS_NUMBER = 5
TRAITS_NUMBER_WITHOUT_CALORIES = TRAITS_NUMBER - 1
CALORIES = 4


def load_input_file(file_name: str):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def parse_input(lines: [str]):
    pattern = re.compile(r'\w+: capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)')
    for line in lines:
        groups = pattern.match(line)
        yield tuple(map(int, [groups[g + 1] for g in range(TRAITS_NUMBER)]))


def proportion_generator(number_of_ingredients: int):


    def build_proportion_list(tab, position, size, result):
        if position + 1 == size:
            tab[position] = 0
            tab[position] = 100 - sum(tab)
            result.append(tab)
        else:
            limit = sum(tab)
            for t in range(0, 101 - limit):
                tab[position] = t
                build_proportion_list(tab[:], position + 1, size, result)


    proportions = []
    build_proportion_list([0] * number_of_ingredients, 0, number_of_ingredients, proportions)

    for proportion in proportions:
        yield proportion


def calculate_score(proportion: [int], ingredients: [tuple], number_of_ingredients: int):
    traits = map(
        lambda t: t if t > 0 else 0,
        [sum(proportion[index] * ingredients[index][trait] for index in range(number_of_ingredients))
        for trait in range(TRAITS_NUMBER_WITHOUT_CALORIES)]
    )

    return functools.reduce(operator.mul, traits, 1)


def solution_for_first_part(lines: [str]):
    ingredients = list(parse_input(lines))
    number_of_ingredients = len(ingredients)

    return max(
        calculate_score(proportion, ingredients, number_of_ingredients)
        for proportion in proportion_generator(number_of_ingredients)
    )


def solution_for_second_part(lines: [str]):


    def calculate_calories(proportion: [int], ingredients: [tuple], number_of_ingredients: int):
        return sum(
                proportion[index] * ingredients[index][CALORIES]
                for index in range(number_of_ingredients)
            )


    REQUESTED_CALORIES_NUMBER = 500
    ingredients = list(parse_input(lines))
    number_of_ingredients = len(ingredients)

    return max(
            calculate_score(proportion, ingredients, number_of_ingredients)
            for proportion in proportion_generator(number_of_ingredients)
            if calculate_calories(proportion, ingredients, number_of_ingredients) == REQUESTED_CALORIES_NUMBER
        )


# The input is taken from: https://adventofcode.com/2015/day/15/input
print("Solution for the first part:", solution_for_first_part(load_input_file('input.15.txt')))
print("Solution for the second part:", solution_for_second_part(load_input_file('input.15.txt')))
