import re


def file_to_input_list(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def parse_input(lines: [str]):
    pattern = re.compile(r'^([a-z]+) (([a-z])|(-?\d+)) (([a-z])|(-?\d+))$')

    for line in lines:
        match = pattern.match(line)

        two = match[3] or int(match[4])
        third = match[6] or int(match[7])

        yield match[1], two, third
        

def register_or_value(input, registers: {}) -> int:
    return registers[input] if input in registers else input


def instruction_set(registers, a, b) -> int:
    registers[a] = register_or_value(b, registers)
    return 1


def instruction_sub(registers, a, b) -> int:
    registers[a] -= register_or_value(b, registers)
    return 1


def instruction_mul(registers, a, b) -> int:
    registers[a] *= register_or_value(b, registers)
    return 1


def instruction_jnz(registers, a, b) -> int:
    return register_or_value(b, registers) if register_or_value(a, registers) != 0 else 1


def run_program(input_program: [str]):
    mul_instruction_counter = 0

    program = [instruction_tuple for instruction_tuple in parse_input(input_program)]
    registers = {i: 0 for i in 'abcdefgh'}
    functions = {
        name[len('instruction_'):]: value
        for name, value in globals().items()
        if name.startswith('instruction_')
    }

    program_length = len(program)
    index = 0

    while index >= 0 and index < program_length:
        name, x, y = program[index]
        if name == 'mul':
            mul_instruction_counter += 1

        function = functions[name]
        index += function(registers, x, y)

    return mul_instruction_counter


print('Solution for the first part:', run_program(file_to_input_list('input.23.txt')))


def transcibe_program(input_program: [str]):
    program = [instruction_tuple for instruction_tuple in parse_input(input_program)]

    index = 0
    for name, x, y in program:
        print('_' + str(index).zfill(2) + ': ', end='')

        if name == 'set':
            print(f'{x} = {y}')
        elif name == 'sub':
            print(f'{x} -= {y}')
        elif name == 'mul':
            print(f'{x} *= {y}')
        elif name == 'jnz':
            print(f'if ({x} != 0) goto :_{str(index + y).zfill(2)}')

        index += 1

# Translate input:
# transcibe_program(file_to_input_list('input.23.txt'))

# then analized and transfered into:
b_start = 100000 + '<value_from_first_line_of_input>' * 100
h = 0
for b in range(b_start, b_start + 17000 + 1, 17):
    for d in range(2, b):
        if b % d == 0:
            e = b // d
            if e >= 2 and e < b:
                h += 1
            break

print('Solution for the second part:', h)
