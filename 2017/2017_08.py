import re


def parser(file_name):
    pattern = re.compile(r'^([a-z]+) (inc|dec) (-?\d+) if ([a-z]+) (!=|==|>=|<=|<|>) (-?\d+)\n$')

    with open(file_name) as file:
        for line in file:
            group = pattern.match(line)
            yield group[4], group[5], int(group[6]), group[1], group[2], int(group[3])


def check_condition(register_value, operant, against_value) -> bool:
    if operant == '!=':
        return register_value != against_value
    elif operant == '==':
        return register_value == against_value
    elif operant == '>=':
        return register_value >= against_value
    elif operant == '<=':
        return register_value <= against_value
    elif operant == '<':
        return register_value < against_value
    elif operant == '>':
        return register_value > against_value

    raise TypeError(f'unknown operant: {operant}')


def calculate_register_value(register_value, operant, how_much) -> int:
    if operant == 'inc':
        return register_value + how_much
    elif operant == 'dec':
        return register_value - how_much

    raise TypeError(f'unknown operant: {operant}')


def do_program(source_input, registers):
    for line in source_input:
        condition_register_name = line[0]
        condition_register_value = registers.get(condition_register_name, 0)

        if check_condition(condition_register_value, line[1], line[2]):
            register_name = line[3]
            register_value = registers.get(register_name, 0)
            value = calculate_register_value(register_value, line[4], line[5])
            registers[register_name] = value
            yield value

    return registers


registers = {}
the_greated_value = 0
for value in do_program(parser('input.txt'), registers):
    if value > the_greated_value:
        the_greated_value = value

largest = max(registers.values())
print(f"Largest value in register: {the_greated_value}")
print(f"Largest in registers after: {largest}")
