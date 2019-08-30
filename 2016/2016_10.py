import re


def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


class Factory:

    def __init__(self):
        self.values = None
        self.instructions = None

    def add_value_to_bot(self, bot_name, value):
        tmp = self.values.get(bot_name, [])
        tmp.append(value)

        self.values[bot_name] = tmp

    def parse_line(self, lines: [str]):
        value_line = re.compile(r'value (\d+) goes to bot (\d+)')
        instruction_line = re.compile(r'bot (\d+) gives low to ((bot|output) (\d+)) and high to ((bot|output) (\d+))')

        self.values = {}
        self.instructions = {}

        for line in lines:
            if line.startswith('value'):
                groups = value_line.match(line)
                bot_name = f'bot {groups[2]}'

                self.add_value_to_bot(bot_name, int(groups[1]))
            else:
                groups = instruction_line.match(line)
                self.instructions[f'bot {groups[1]}'] = (groups[2], groups[5])
        
    def follow_instruction(self):
        while True:
            key = next((key for key, value in self.values.items() if len(value) == 2 and key.startswith('bot ')), None)
            if key == None:
                return

            low_value, high_value = sorted(self.values[key])

            yield key, low_value, high_value

            low_value_bot, high_value_bot = self.instructions[key]

            self.values[key] = []
            self.add_value_to_bot(low_value_bot, low_value)
            self.add_value_to_bot(high_value_bot, high_value)


def solution_for_the_first_part(factory: Factory) -> str:
    for bot_name, low_value, high_value in factory.follow_instruction():
        if low_value == 17 and high_value == 61:
            return bot_name


def solution_for_the_second_part(factory: Factory) -> int:
    for _ in factory.follow_instruction():
        pass
    
    return factory.values['output 0'][0] * factory.values['output 1'][0] * factory.values['output 2'][0]


# The input is taken from: https://adventofcode.com/2016/day/10/input
factory = Factory()
factory.parse_line(load_input_file('input.10.txt'))
print("Solution for the first part:", solution_for_the_first_part(factory))
print("Solution for the second part:", solution_for_the_second_part(factory))
