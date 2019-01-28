import re
import functools
import operator


TRAITS_NUMBER_WITHOUT_CALORIES = 4


def load_input_file(file_name: str):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def receptie_score_generator(lines: [str]):


    def parse_input(lines: [str]):
        pattern = re.compile(r'\w+: capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)')
        for line in lines:
            groups = pattern.match(line)
            yield tuple(map(int, [groups[g + 1] for g in range(5)]))


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


    ingredients = list(parse_input(lines))
    number_of_ingredients = len(ingredients)

    proportions = []
    build_proportion_list([0] * number_of_ingredients, 0, number_of_ingredients, proportions)

    for proportion in proportions:
        traits = map(
            lambda t: t if t > 0 else 0,
            [sum(proportion[index] * ingredients[index][trait] for index in range(number_of_ingredients))
            for trait in range(TRAITS_NUMBER_WITHOUT_CALORIES)]
        )

        yield functools.reduce(operator.mul, traits, 1)


# The solution is taken from: https://adventofcode.com/2015/day/15/input
print("Solution for the first part:", max(score for score in receptie_score_generator(load_input_file('input.15.txt'))))
