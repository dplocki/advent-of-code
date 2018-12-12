def parse_rules(input: str) -> {}:
    return {tuple([bool(x == '#') for x in line[0:5]]): line[-1] == '#' for line in input.split('\n')}


def input_begin_state(input: str) -> {}:
    return { i: p == '#'  for i, p in enumerate(input)}


def run_generation(rules, begin_state):
    start_index = 0
    end_index = len(begin_state) - 1
    actual_state = begin_state

    while True:
        new_state = {}

        for index in range(start_index, end_index + 1):
            neighbours = tuple([actual_state.get(i, False) for i in range(index - 2, index + 3)])
            new_state[index] = rules.get(neighbours, False)

        start_index -= 2
        end_index += 2

        actual_state = new_state
        yield actual_state


def calculate_sum_of_pots_numbers(state: {}) -> int:
    return sum([index for index, is_pot in state.items() if is_pot])


def solution_for_first_part(unparsed_rules, begin_state):
    rules = parse_rules(unparsed_rules)
    begin_state = input_begin_state(begin_state)

    generator = run_generation(rules, begin_state)

    for _ in range(19):
        next(generator)

    generation_20th_state = next(generator)
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
unparsed_rules = '''<input>'''
unparsed_begin_state = '<input>'

print("Solution for first part:", solution_for_first_part(unparsed_rules, unparsed_begin_state))

rules = parse_rules(unparsed_rules)
begin_state = input_begin_state(unparsed_begin_state)

# generation_generator = run_generation(rules, begin_state)
# i = 1
# while True:
#     generation = next(generation_generator)
#     temp = calculate_sum_of_pots_numbers(generation)
#     if i % 1000 == 0:
#         print(f"test({i}, {temp})")
#     i += 1

#     if i == 5001:
#         break


def calulate_1000_multiplication(for_number: int) -> int:
    t = int(for_number / 1000)
    return (t * 36 - 1) * 1000 + 458


def test(generation_number, excepted_result):
    result = calulate_1000_multiplication(generation_number)
    assert result == excepted_result, f"{result} but excepted {excepted_result} for {generation_number}"


test(1000, 35458)
test(2000, 71458)
test(3000, 107458)
test(4000, 143458)
test(5000, 179458)

print("Solution for second part:", calulate_1000_multiplication(50000000000))
