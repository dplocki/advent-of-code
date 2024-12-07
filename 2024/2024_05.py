from typing import Iterable, Set, Tuple, Union


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


def check_the_update_pages_list(order_rules: Set[Tuple[int, int]], update_pages: Tuple[Tuple[int]]) -> Union[int, None]:
    for index, value in enumerate(update_pages):
        for other_index in range(index, len(update_pages)):
            if (update_pages[other_index], value) in order_rules:
                return index

    return None


def solution_for_first_part(task_input: str) -> int:
    order_rules, updates_pages = parse(task_input)

    return sum(
        update_pages[len(update_pages) // 2]
        for update_pages in updates_pages
        if check_the_update_pages_list(order_rules, update_pages) == None)


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
print("Solution for the first part:", solution_for_first_part(task_input))


def find_matching_index(order_rules: Set[Tuple[int, int]], update_pages: Tuple[Tuple[int]], number: int) -> int:
    for index, value in enumerate(update_pages):
        if (number, value) in order_rules:
            return index

    return len(update_pages)


def fix_order_page_update_list(order_rules: Set[Tuple[int, int]], update_pages: Tuple[Tuple[int]]) -> Iterable[int]:
    incorrect_values = []
    only_correct_values = update_pages[:]

    index = check_the_update_pages_list(order_rules, only_correct_values)

    while index != None:
        incorrect_values.append(only_correct_values[index])
        only_correct_values = only_correct_values[:index] + only_correct_values[index + 1:]

        index = check_the_update_pages_list(order_rules, only_correct_values)

    result = only_correct_values[:]

    for value_to_retry in incorrect_values:
        index = find_matching_index(order_rules, result, value_to_retry)
        result = list(result[:index]) + [value_to_retry] + list(result[index:])

    return result


def solution_for_second_part(task_input: str) -> int:
    order_rules, updates_pages = parse(task_input)
    result = 0

    for update_pages in updates_pages:
        incorrect_index = check_the_update_pages_list(order_rules, update_pages)
        if incorrect_index == None:
            continue

        correct_page_update_list = fix_order_page_update_list(order_rules, update_pages)
        result += correct_page_update_list[len(correct_page_update_list) // 2]

    return result


assert solution_for_second_part(example_input) == 123
print("Solution for the second part:", solution_for_second_part(task_input))
