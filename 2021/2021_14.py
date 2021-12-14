from typing import Counter


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def parse(task_input: str) -> tuple[str, list[tuple[str, str]]]:
    tokens = task_input.split('\n\n')

    return tokens[0], [tuple(line.split(' -> ')) for line in tokens[1].splitlines()]


def solution_for_first_part(task_input: tuple[str, list[tuple[str, str]]]) -> int:
    template, rules = parse(task_input)

    for _ in range(10):
        new_template = ''
        for left, right in zip(template, template[1:]):
            x = left + right
            y = next(rule for rule in rules if x == rule[0])

            new_template += left + y[1]

        new_template += right
        template = new_template    

    quantity = Counter(template).values()
    max_value = max(quantity)
    min_value = min(quantity)

    return max_value - min_value


example_input = '''NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C'''

assert solution_for_first_part(example_input) == 1588

# The input is taken from: https://adventofcode.com/2021/day/14/input
task_input = load_input_file('input.14.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
