import re


def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse_line(lines: [str]):
    value_line = re.compile(r'value (\d+) goes to bot (\d+)')
    instruction_line = re.compile(r'bot (\d+) gives low to ((bot|output) (\d+)) and high to ((bot|output) (\d+))')

    initial_values = {}
    instructions = {}

    for line in lines:
        if line.startswith('value'):
            groups = value_line.match(line)
            bot_name = f'bot {groups[2]}'

            bot = initial_values.get(bot_name, [])
            bot.append(int(groups[1]))
            initial_values[bot_name] = bot
        else:
            groups = instruction_line.match(line)
            instructions[f'bot {groups[1]}'] = (groups[2], groups[5])

    return instructions, initial_values


def follow_instruction(instructions: {}, values: {}):


    def add_value_to_bot(bot_name, value):
        tmp = values.get(bot_name, [])
        tmp.append(value)

        values[bot_name] = tmp


    while True:
        key = next(key for key, value in values.items() if len(value) == 2 and key.startswith('bot '))
        low_value, high_value = sorted(values[key])

        yield key, low_value, high_value

        low_value_bot, high_value_bot = instructions[key]

        values[key] = []
        add_value_to_bot(low_value_bot, low_value)
        add_value_to_bot(high_value_bot, high_value)


def solution_for_the_first_part(instructions: {}, values: {}):
    for bot_name, low_value, high_value in follow_instruction(instructions, values):
        if low_value == 17 and high_value == 61:
            return bot_name


# The input is taken from: https://adventofcode.com/2016/day/10/input
instructions, initial_values = parse_line(load_input_file('input.10.txt'))
print("Solution for the first part:", solution_for_the_first_part(instructions, initial_values))
