def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def parse(task_input: [str]) -> tuple:
    
    def parse_rule_line(line: [str]) -> [int]:
        _, tokens = line.split(': ')
        tokens = tokens.split(' ')
        return list(map(int, tokens[0].split('-') + tokens[2].split('-')))

    def parse_your_ticket(lines):
        return map(int, lines[1].split(','))

    def parse_tickets(lines):
        for line in lines[1:]:
            yield map(int, line.split(','))


    sections = list(map(str.splitlines, task_input.split('\n\n')))
    return list(map(parse_rule_line, sections[0])), \
        list(parse_your_ticket(sections[1])), \
        list(parse_tickets(sections[2]))


def solution_for_first_part(task_input: [str]) -> int:
    rules, _, tickets = parse(task_input)

    return sum(
        number
        for ticket in tickets
        for number in ticket
        if not any((r[0] <= number <= r[1]) or (r[2] <= number <= r[3]) for r in rules))


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
