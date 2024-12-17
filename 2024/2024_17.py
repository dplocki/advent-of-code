import re
from typing import Dict, Iterable, Tuple


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def parse(task_input: Iterable[str]) -> Tuple[Dict[str, int], Tuple[int]]:
    PATTERN = 'Register ([A-Z]): (\d+)'
    raw_registers, program_line = task_input.split('\n\n')

    return { name: int(value) for name, value in re.findall(PATTERN, raw_registers) }, tuple(map(int, program_line.split(' ')[1].split(',')))


def get_value_combo_operand(registers: Dict[str, int], operand: int) -> int:
    if 0 <= operand <= 3:
        return operand
    if operand == 4:
        return registers['A']
    if operand == 5:
        return registers['B']
    if operand == 6:
        return registers['C']

    raise Exception('opt code 7')


def run_program(registers: Dict[str, int], instructions: Tuple[int, ...]) -> Tuple[str, Dict[str, int]]:
    instruction_pointer = 0
    output = []

    while instruction_pointer < len(instructions):
        optcode = instructions[instruction_pointer]
        operant = instructions[instruction_pointer + 1]

        if optcode == 0:
            registers['A'] = registers['A'] // 2 ** get_value_combo_operand(registers, operant)
        elif optcode == 1:
            registers['B'] = registers['B'] ^ operant
        elif optcode == 2:
            registers['B'] = get_value_combo_operand(registers, operant) % 8
        elif optcode == 3:
            if registers['A'] != 0:
                instruction_pointer = operant
                continue
        elif optcode == 4:
            registers['B'] = registers['B'] ^ registers['C']
        elif optcode == 5:
            output.append(get_value_combo_operand(registers, operant) % 8)
        elif optcode == 6:
            registers['B'] = registers['A'] // 2 ** get_value_combo_operand(registers, operant)
        elif optcode == 7:
            registers['C'] = registers['A'] // 2 ** get_value_combo_operand(registers, operant)
        else:
            break

        instruction_pointer += 2

    return ','.join(map(str, output)), registers


def solution_for_first_part(task_input: Iterable[str]) -> int:
    registers, instructions = parse(task_input)
    return run_program(registers, instructions)[0]


example_input = '''Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0'''

assert solution_for_first_part(example_input) == '4,6,3,5,6,3,5,2,1,0'

# The input is taken from: https://adventofcode.com/2024/day/17/input
task_input = load_input_file('input.17.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
