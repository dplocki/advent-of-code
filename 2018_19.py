import re
opcodes = __import__('2018_16')


def parse_input(input: [str]):
    pattern = re.compile(r'^([a-z]+) (\d+) (\d+) (\d+)$')

    for line in input:
        result = pattern.match(line)
        yield result[1], int(result[2]), int(result[3]), int(result[4])


def input_to_program(input: [str]):
    return [i for i in parse_input(input)]


def run_program(program: [str], instruction_pointer_register, registers = None, instruction_pointer = None):
    registers = registers or [0] * 6
    instruction_pointer = instruction_pointer or 0

    while instruction_pointer < len(program) and instruction_pointer >= 0:
        print(instruction_pointer, registers)
        instruction = program[instruction_pointer]

        registers[instruction_pointer_register] = instruction_pointer
        registers = opcodes.opcodes[instruction[0]](registers, instruction)
        instruction_pointer = registers[instruction_pointer_register]

        instruction_pointer += 1

    return registers


test_input = input_to_program('''seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5'''.splitlines())

assert run_program(test_input, 0) == [6, 5, 6, 0, 0, 9]

# The input taken from: https://adventofcode.com/2018/day/19/input (without first line)
task_input = input_to_program('''<input>'''.splitlines())

# Second parameter taken from first line of input (as number)
print("Solution for first part:", run_program(task_input, 5)[0])

# to analyze output (kill after a while)
run_program(task_input, 5, [1] + [0] * 5)[0]
