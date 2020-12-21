from collections import defaultdict


def load_input_file(file_name: str) -> [str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: [str]):
    for line in task_input:
        ingri, alergen = line.split(' (contains ')

        yield ingri.split(), alergen[:-1].split(', ')


def solution_for_first_part(task_input):
    foods = list(parse(task_input))

    ingredients_counter = {}
    suspecting_allergens = {}
    for ingredients, allergens in foods:
        for allergen in allergens:
            if allergen in suspecting_allergens:
                suspecting_allergens[allergen] &= set(ingredients)
            else:
                suspecting_allergens[allergen] = set(ingredients)

        for ingredient in ingredients:
            ingredients_counter[ingredient] = ingredients_counter.get(ingredient, 0) + 1

    discovered = {}
    while len(discovered) < len(suspecting_allergens):
        discover_allergen, discovere_ingredient = next(
            (allergen, ingredients.pop())
            for allergen, ingredients in suspecting_allergens.items()
            if len(ingredients) == 1)

        discovered[discover_allergen] = discovere_ingredient
        for allergen, ingredients in suspecting_allergens.items():
            suspecting_allergens[allergen].discard(discovere_ingredient)
 
    return sum(how_much for ingredient, how_much in ingredients_counter.items() if ingredient not in discovered.values())


example_input = '''mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)'''.splitlines()

assert solution_for_first_part(example_input) == 5

# The input is taken from: https://adventofcode.com/2020/day/21/input
task_input = list(load_input_file('input.21.txt'))
result = solution_for_first_part(task_input)
print("Solution for the first part:", result)
