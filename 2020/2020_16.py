from functools import reduce 
from operator import mul


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def parse(task_input: [str]) -> tuple:
    
    def parse_rule_line(line: [str]) -> [int]:
        what, tokens = line.split(': ')
        tokens = tokens.split(' ')
        return what, list(map(int, tokens[0].split('-') + tokens[2].split('-')))

    def parse_your_ticket(lines):
        return map(int, lines[1].split(','))

    def parse_tickets(lines):
        yield from (list(map(int, line.split(','))) for line in lines[1:])


    sections = list(map(str.splitlines, task_input.split('\n\n')))
    return {name:rule for name, rule in map(parse_rule_line, sections[0])}, \
        list(parse_your_ticket(sections[1])), \
        list(parse_tickets(sections[2]))


def check_rule(number: int, rule: [int]) -> bool:
    return (rule[0] <= number <= rule[1]) or (rule[2] <= number <= rule[3])


def solution_for_first_part(task_input: [str]) -> int:
    rules, _, tickets = parse(task_input)

    return sum(
        number
        for ticket in tickets
        for number in ticket
        if not any(check_rule(number, rule) for rule in rules.values()))


example_input = '''class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12'''

assert solution_for_first_part(example_input) == 71

# The input is taken from: https://adventofcode.com/2020/day/16/input
task_input = load_input_file('input.16.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


def deduct_ticket_number_meaning(task_input):
    rules, your_ticket, tickets = parse(task_input)
    possibility = {
        name: set(range(len(your_ticket)))
        for name in rules.keys()
    }

    for ticket in tickets:
        for position, number in enumerate(ticket):
            result = {name: check_rule(number, rule) for name, rule in rules.items()}
            if not any(result.values()):
                continue

            for name, can_be in result.items():
                if not can_be:
                    possibility[name].discard(position)

    result = {}
    while len(result) < len(your_ticket):
        for name, numbers in possibility.items():
            if len(numbers) == 1 and name not in result:
                position = numbers.pop()
                result[name] = position
                for p in possibility.values():
                    p.discard(position)

    return {n:your_ticket[v] for n, v in result.items()}


def solution_for_second_part(task_input: [str]) -> int:
    return reduce(mul, (value
            for name, value in deduct_ticket_number_meaning(task_input).items()
            if 'departure' in name))


example_part2_input = '''class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9'''

assert deduct_ticket_number_meaning(example_part2_input) == { 'class': 12, 'row': 11, 'seat': 13 }

print("Solution for the second part:", solution_for_second_part(task_input))
