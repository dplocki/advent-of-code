def load_input_file(file_name: str):
    with open(file_name) as file:
        return file.read().strip()


def load_input_file(file_name: str):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(lines: [str]):

    def parse_inside_bag(rule: str) -> (int, [str]):
        how_many, what = rule.split(' ', 1)
        return int(how_many), ' '.join(what.split(' ')[:2])


    for line in lines:
        main_bag, rule = line.split(' bags contain ')
        inside_bags = rule.split(', ')
        yield main_bag, [parse_inside_bag(bag) for bag in inside_bags if bag != 'no other bags.']


def can_contain_shiny_gold(bags_rule_set: dict, bag: str) -> bool:
    rules = bags_rule_set[bag]

    if 'shiny gold' in (bag_inside[1] for bag_inside in rules):
        return True
    
    return any(can_contain_shiny_gold(bags_rule_set, bag_inside[1]) for bag_inside in rules)


def solution_for_first_part(bags_rule_set: dict) -> int:
    return sum(1 for bag_name in bags_rule_set.keys() if can_contain_shiny_gold(bags_rule_set, bag_name))


# The input is taken from: https://adventofcode.com/2020/day/7/input
bags_rule_set = { bag: contains for bag, contains in parse(load_input_file('input.07.txt')) }
print("Solution for the first part:", solution_for_first_part(bags_rule_set))
