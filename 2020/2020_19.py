import itertools


class SimpleRule():

    def __init__(self, character):
        self.character = character

    def parse(self, _, message):
        return [message[1:]] if len(message) > 0 and self.character == message[0] else []


class OtherRule():

    def __init__(self, rule_index):
        self.rule_index = rule_index

    def parse(self, rules, message):
        return rules[self.rule_index].parse(rules, message)


class ChainRule():
    
    def __init__(self, rules):
        self.rules = rules
    
    def parse(self, rules, message):
        result = [message]
        for token in self.rules:
            result = list(itertools.chain(*[rules[token].parse(rules, r) for r in result]))
            if not result:
                return []

        return result


class OrRule():
    
    def __init__(self, parts):
        self.parts = parts

    def parse(self, rules, message):
        return list(itertools.chain(*[part.parse(rules, message) for part in self.parts]))


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def parse_rule(raw_rule: str):
    if '"' in raw_rule:
        return SimpleRule(raw_rule[1])
    elif '|' in raw_rule:
        return OrRule([ChainRule(list(map(int, x.split()))) for x in raw_rule.split(' | ')])
    elif ' ' in raw_rule:
        return ChainRule(list(map(int, raw_rule.split())))

    return OtherRule(int(raw_rule))


def parse(task_input: [str]):

    raw_rules, raw_messages = task_input.split('\n\n')

    rules = {}
    for rule in raw_rules.splitlines():
        raw_rule_index, rule = rule.split(': ')
        rules[int(raw_rule_index)] = parse_rule(rule)

    return rules, raw_messages.splitlines()


def count_valid_message(rules: dict, messages: [str]) -> int:
    return sum(1 for message in messages if '' in rules[0].parse(rules, message))


def solution_for_first_part(task_input: str) -> int:
    rules, messages = parse(task_input)
    return count_valid_message(rules, messages)


first_part_example_input = '''0: 4 1 5
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

assert solution_for_first_part(first_part_example_input) == 2

#The input is taken from: https://adventofcode.com/2020/day/19/input
task_input = load_input_file('input.19.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input):
    rules, messages = parse(task_input)

    rules[8] = parse_rule('42 | 42 8')
    rules[11] = parse_rule('42 31 | 42 11 31')

    return count_valid_message(rules, messages)


second_part_example_input = '''42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba'''

assert solution_for_second_part(second_part_example_input) == 12
print("Solution for the second part:", solution_for_second_part(task_input))
