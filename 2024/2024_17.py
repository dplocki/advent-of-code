from typing import Dict, Tuple
from itertools import count
import re


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def parse(task_input: str) -> Tuple[Dict[str, int], Tuple[int]]:
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


def solution_for_first_part(task_input: str) -> int:
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


example_input = '''Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0'''


def solution_for_second_part(task_input: str) -> int:
    # Brute-force attempt, too slow for final answer

    registers, instructions = parse(task_input)
    requested_output = ','.join(map(str, instructions))

    for a_value in count(8 ** (len(instructions) - 1)):
        tmp_registers = {
            'A': a_value,
            'B': registers['B'],
            'C': registers['C'],
        }

        output = run_program(tmp_registers, instructions)[0]
        if requested_output == output:
            return a_value


assert solution_for_second_part(example_input) == 117440


def calculate_output(current_value_a: int, digit: int) -> int:
    A = current_value_a * 8 + digit

    #
    # Place translated to Python program here
    #

    return B % 8


def solution_for_second_part(task_input: str):
    _, instructions = parse(task_input)
    results = [ 0 ]

    for program_code in reversed(instructions):
        results = [
            (current_value_a * 8 + digit)
            for current_value_a in results
            for digit in range(8)
            if calculate_output(current_value_a, digit) == program_code
        ]

    return min(results)


print("Solution for the second part:", solution_for_second_part(task_input))