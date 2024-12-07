from typing import Set, Tuple


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def parse(task_input: str) -> Tuple[Set[Tuple[int, int]], Tuple[Tuple[int]]]:
    first_section, second_section = task_input.split('\n\n')

    order_rules = {
        tuple(map(int, line.split('|')))
        for line in first_section.splitlines()}

    updates_pages = tuple(
        tuple(map(int, line.split(',')))
        for line in second_section.splitlines())

    return order_rules, updates_pages


def check_the_update_pages_list(order_rules: Set[Tuple[int, int]], update_pages: Tuple[Tuple[int]]) -> bool:
    for index, value in enumerate(update_pages):
        for other_index in range(index, len(update_pages)):
            if (update_pages[other_index], value) in order_rules:
                return False

    return True


def solution_for_first_part(task_input: str) -> int:
    order_rules, updates_pages = parse(task_input)

    return sum(
        update_pages[len(update_pages) // 2]
        for update_pages in updates_pages
        if check_the_update_pages_list(order_rules, update_pages))


example_input = '''47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47'''

assert solution_for_first_part(example_input) == 143

# The input is taken from: https://adventofcode.com/2024/day/5/input
task_input = load_input_file('input.05.txt')
result = solution_for_first_part(task_input)
print("Solution for the first part:", result)
