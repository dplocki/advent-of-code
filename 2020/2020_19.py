memory = None
memory_rules = None


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def parse(task_input: [str]):
    raw_rules, raw_messages = task_input.split('\n\n')

    rules = {}
    for rule in raw_rules.splitlines():
        raw_rule_index, rule = rule.split(': ')
        rules[int(raw_rule_index)] = rule

    return rules, raw_messages.splitlines()


def memoize(func):

    def inner(rules, rule, message) -> int:
        if (rule, message) not in memory:
            memory[(rule, message)] = func(rules, rule, message)

        return memory[(rule, message)]


    return inner


@memoize
def check_rule(rules, rule, message) -> bool:
    if rule.isnumeric():
        return check_rule(rules, rules[int(rule)], message)

    if '|' in rule:
        tokens = rule.split(' | ')
        return check_rule(rules, tokens[0], message) or check_rule(rules, tokens[1], message)

    if ' ' in rule:
        tokens = rule.split(' ')

        for i in range(1, len(message)):
            if check_rule(rules, tokens[0], message[:i]):
                return check_rule(rules, ' '.join(tokens[1:]), message[i:])

        return False

    return rule[1] == message


def solution_for_first_part(task_input):
    global memory

    memory = {}
    rules, messages = parse(task_input)
    return sum(1 for message in messages if check_rule(rules, '0', message))


example_input = '''0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb'''

assert solution_for_first_part(example_input) == 2

#The input is taken from: https://adventofcode.com/2020/day/19/input
task_input = load_input_file('input.19.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
