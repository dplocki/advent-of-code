def parse_rules(input: str) -> {}:
    return {tuple([bool(x == '#') for x in line[0:5]]): line[-1] == '#' for line in input.split('\n')}


def input_begin_state(input: str) -> {}:
    return { i: p == '#'  for i, p in enumerate(input)}


def run_20_generation(rules, begin_state):
    start_index = 0
    end_index = len(begin_state) - 1
    actual_state = begin_state

    for _ in range(20):
        new_state = {}

        for index in range(start_index, end_index + 1):
            neighbours = tuple([actual_state.get(i, False) for i in range(index - 2, index + 3)])
            new_state[index] = rules.get(neighbours, False)

        start_index -= 2
        end_index += 2

        actual_state = new_state

    return actual_state


def calculate_sum_of_pots_numbers(state: {}) -> int:
    return sum([index for index, is_pot in state.items() if is_pot])


def solution_for_first_part(unparsed_rules, begin_state):
    rules = parse_rules(unparsed_rules)
    begin_state = input_begin_state(begin_state)
    generation_20th_state = run_20_generation(rules, begin_state)

    return calculate_sum_of_pots_numbers(generation_20th_state)


test_input_rules = '''...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #'''

test_input_begin = '#..#.#..##......###...###'

assert solution_for_first_part(test_input_rules, test_input_begin) == 325

# The input is taken from: https://adventofcode.com/2018/day/12/input
print("Solution for first part:", solution_for_first_part('''<rules_input>''', '<initial_state_input>'))
