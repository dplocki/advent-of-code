from typing import Callable


YOUR_BAG = 'shiny gold'


def load_input_file(file_name: str):
    with open(file_name) as file:
        return file.read().strip()


def load_input_file(file_name: str):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(lines: [str]) -> [str]:

    def parse_inside_bag(rule: str) -> (int, [str]):
        how_many, what = rule.split(' ', 1)
        return int(how_many), ' '.join(what.split(' ')[:2])


    for line in lines:
        main_bag, rule = line.split(' bags contain ')
        inside_bags = rule.split(', ')
        yield main_bag, [parse_inside_bag(bag) for bag in inside_bags if bag != 'no other bags.']


def memoize(func: Callable[[str], int]) -> Callable[[str], int]:
    memory = {}

    def inner(bag_name: str) -> int:
        if bag_name not in memory:
            memory[bag_name] = func(bag_name)

        return memory[bag_name]

    return inner


def solution_for_first_part(bags_rule_set: dict) -> int:

    @memoize
    def can_contain_shiny_gold(bag: str) -> bool:
        rules = bags_rule_set[bag]

        if YOUR_BAG in (bag_inside[1] for bag_inside in rules):
            return True

        return any(can_contain_shiny_gold(bag_inside[1]) for bag_inside in rules)


    return sum(1 for bag_name in bags_rule_set.keys() if can_contain_shiny_gold(bag_name))


# The input is taken from: https://adventofcode.com/2020/day/7/input
bags_rule_set = { bag: contains for bag, contains in parse(load_input_file('input.07.txt')) }
print("Solution for the first part:", solution_for_first_part(bags_rule_set))


def solution_for_second_part(bags_rule_set: dict) -> int:

    @memoize
    def count(bag_name: str) -> int:
        inside_bags = bags_rule_set[bag_name]
        return sum(bag[0] + bag[0] * count(bag[1]) for bag in inside_bags)


    return count(YOUR_BAG)


print("Solution for the second part:", solution_for_second_part(bags_rule_set))
