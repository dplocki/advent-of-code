from collections import defaultdict


def load_input_file(file_name: str) -> [str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: [str]):
    for line in task_input:
        ingri, alergen = line.split(' (contains ')

        yield ingri.split(), alergen[:-1].split(', ')


def analyze_food(task_input: [str]) -> tuple:
    ingredients_counter = {}
    suspecting_allergens = {}
    for ingredients, allergens in parse(task_input):
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

    return discovered, ingredients_counter


def solution_for_first_part(task_input):
    discovered, ingredients_counter = analyze_food(task_input)
 
    return sum(how_much for ingredient, how_much in ingredients_counter.items() if ingredient not in discovered.values())


example_input = '''mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)'''.splitlines()

assert solution_for_first_part(example_input) == 5

# The input is taken from: https://adventofcode.com/2020/day/21/input
task_input = list(load_input_file('input.21.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input):
    discovered, _ = analyze_food(task_input)

    return ','.join(discovered[name] for name in sorted(discovered.keys()))


assert solution_for_second_part(example_input) == 'mxmxvkd,sqjhc,fvjkl'
print("Solution for the second part:", solution_for_second_part(task_input))
