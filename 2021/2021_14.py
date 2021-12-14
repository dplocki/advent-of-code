from collections import defaultdict


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def parse(task_input: str) -> tuple[str, list[tuple[str, str]]]:
    tokens = task_input.split('\n\n')

    return tokens[0], [tuple(line.split(' -> ')) for line in tokens[1].splitlines()]


def polymerization(task_input: str) -> list[tuple[dict[str, int], str]]:
    template, rules_raw = parse(task_input)
    
    last_element = template[-1]
    rules = {rule[0]:rule[1] for rule in rules_raw}

    pair_counter = defaultdict(int)
    for a, b in zip(template, template[1:]):
        pair_counter[a + b] += 1

    while True:
        new_pair_counter = defaultdict(int)

        for pair, how_many in pair_counter.items():
            result = rules[pair]
            new_pair_counter[pair[0] + result] += how_many
            new_pair_counter[result + pair[1]] += how_many

        pair_counter = new_pair_counter
        yield pair_counter, last_element


def find_the_delta(state: tuple[dict[str, int], str]) -> int:
    pair_counter, last_element = state

    elements = defaultdict(int)
    for pair, how_much in pair_counter.items():
        elements[pair[0]] += how_much

    elements[last_element] += 1

    quantity = elements.values()
    max_value = max(quantity)
    min_value = min(quantity)

    return max_value - min_value


def solution_for_first_part(task_input: str) -> int:
    for state, _ in zip(polymerization(task_input), range(10)):
        pass

    return find_the_delta(state)


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


def solution_for_second_part(task_input: str) -> int:
    for state, _ in zip(polymerization(task_input), range(40)):
        pass

    return find_the_delta(state)


assert solution_for_second_part(example_input) == 2188189693529
print("Solution for the second part:", solution_for_second_part(task_input))
