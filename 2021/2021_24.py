import math
import itertools
from statistics import variance


def load_input_file(file_name: str) -> list[str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: list[str]):
    for line in task_input:
        tokens = line.split(' ')
        
        if len(tokens) == 3:
            yield tokens[0], tokens[1], int(tokens[2]) if tokens[2] not in 'wxyz' else tokens[2]
        else:
            yield tokens[0], tokens[1], None


def run_program(lines, input_gen, x=0, y=0, z=0):
    """This method is not used in the solution, but it was usefull during analize the problem."""

    def registe_or_value(registers, par):
        if isinstance(par, int):
            return par
        
        return registers[par]


    registers = { 'w': 0, 'x': x, 'y': y, 'z': z }

    for instruction, par1, par2 in lines:
        if instruction == 'add':
            registers[par1] = registers[par1] + registe_or_value(registers, par2)
        elif instruction == 'inp':
            registers[par1] = next(input_gen)
        elif instruction == 'mul':
            registers[par1] = registers[par1] * registe_or_value(registers, par2)
        elif instruction == 'div':
            a = math.trunc(registers[par1] // registe_or_value(registers, par2))
            registers[par1] = a
        elif instruction == 'mod':
            registers[par1] = registers[par1] % registe_or_value(registers, par2)
        elif instruction == 'eql':
            registers[par1] = 1 if registers[par1] == registe_or_value(registers, par2) else 0

    return registers


def load_variables(task_input):
    instructions = list(parse(task_input))

    instructions_per_digit = []
    for instruction in instructions:
        if instruction[0] == 'inp':
            current_digit = []
            instructions_per_digit.append(current_digit)

        current_digit.append(instruction)

    return [(instructions[4][2], instructions[5][2], instructions[15][2]) for instructions in instructions_per_digit]


def check_all_combinations(task_input, digits_collections: list[int]) -> str:
    variables = load_variables(task_input)

    for digits_collection in digits_collections:
        digit_provider = iter(digits_collection)
        result = []
        z = 0
        for p1, p2, p3 in variables:
            digit = None
            if p2 < 0:
                digit = z % 26 + p2
                if digit > 9 or digit < 1:
                    continue

                z //= p1
            else:
                digit = next(digit_provider)
                z = z // p1 * 26 + digit + p3

            result.append(digit)

        if z == 0:
            return ''.join(map(str, result))

    raise Exception('Not found')


def solution_for_first_part(task_input):
    return check_all_combinations(task_input, itertools.product(range(9, 0, -1), repeat=7))


# The input is taken from: https://adventofcode.com/2021/day/24/input
task_input = list(load_input_file('input.24.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input):
    return check_all_combinations(task_input, itertools.product(range(1, 10), repeat=7))


print("Solution for the second part:", solution_for_second_part(task_input))
