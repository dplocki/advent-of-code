import re


A, B, C = 1, 2, 3
INDEX_REG = None


def addr(instructions):
    return f'reg[{instructions[C]}] = reg[{instructions[A]}] + reg[{instructions[B]}]'


def addi(instructions):
    return f'reg[{instructions[C]}] = reg[{instructions[A]}] + {instructions[B]}'


def mulr(instructions):
    return f'reg[{instructions[C]}] = reg[{instructions[A]}] * reg[{instructions[B]}]'


def muli(instructions):
    return f'reg[{instructions[C]}] = reg[{instructions[A]}] * {instructions[B]}'


def banr(instructions):
    return f'reg[{instructions[C]}] = reg[{instructions[A]}] & reg[{instructions[B]}]'


def bani(instructions):
    return f'reg[{instructions[C]}] = reg[{instructions[A]}] & {instructions[B]}'


def borr(instructions):
    return f'reg[{instructions[C]}] = reg[{instructions[A]}] | reg[{instructions[B]}]'


def bori(instructions):
    return f'reg[{instructions[C]}] = reg[{instructions[A]}] | {instructions[B]}'


def setr(instructions):
    return f'reg[{instructions[C]}] = reg[{instructions[A]}]'


def seti(instructions):
    return f'reg[{instructions[C]}] = {instructions[A]}'


def gtir(instructions):
    return f'reg[{instructions[C]}] = 1 if {instructions[A]} > reg[{instructions[B]}] else 0'


def gtri(instructions):
    return f'reg[{instructions[C]}] = 1 if reg[{instructions[A]}] > {instructions[B]} else 0'


def gtrr(instructions):
    return f'reg[{instructions[C]}] = 1 if reg[{instructions[A]}] > reg[{instructions[B]}] else 0'


def eqir(instructions):
    return f'reg[{instructions[C]}] = 1 if {instructions[A]} == reg[{instructions[B]}] else 0'


def eqri(instructions):
    return f'reg[{instructions[C]}] = 1 if reg[{instructions[A]}] == {instructions[B]} else 0'


def eqrr(instructions):
    return f'reg[{instructions[C]}] = 1 if reg[{instructions[A]}] == reg[{instructions[B]}] else 0'


opcodes = {
    'addr': addr,
    'addi': addi,
    'mulr': mulr,
    'muli': muli,
    'banr': banr,
    'bani': bani,
    'borr': borr,
    'bori': bori,
    'setr': setr,
    'seti': seti,
    'gtir': gtir,
    'gtri': gtri,
    'gtrr': gtrr,
    'eqir': eqir,
    'eqri': eqri,
    'eqrr': eqrr
}


def parse_program_file(file_name: str):
    pattern = re.compile(r'(\w+) (\d+) (\d+) (\d+)')
    index_registers = None

    with open(file_name) as file:
        for line in file:
            if line.startswith('#'):
                index_registers = int(line[4:])
            else:
                match = pattern.match(line.strip())
                yield index_registers, match[1], int(match[2]), int(match[3]), int(match[4])


def if_is_jump(index_register: int, instructions: []):
    tmp = opcodes[instructions[0]](instructions)
    if instructions[C] == index_register:
        return tmp.replace(f'reg[{instructions[C]}] = ', 'jump_to ') 

    return tmp


def replace_reg_with_letters(result: str):
    to_replace = {
        f'reg[{i}]': l
        for i, l in zip(range(6), 'ABCDEF')
    }

    for f, t in to_replace.items():
        result = result.replace(f, t)

    return result


def replace_index_with_line_number(index_register, line_number, result: str):
    return result.replace(f'reg[{index_register}]', str(line_number))


def translate_program(file_name: str):
    line_number = 0
    for instructions in parse_program_file(file_name):
        print(
            str(line_number).zfill(2) + ':',
            replace_reg_with_letters(
                replace_index_with_line_number(
                    instructions[0],
                    line_number, 
                    if_is_jump(instructions[0], instructions[1:])))
        )

        line_number += 1


#The input taken from: https://adventofcode.com/2018/day/21/input
translate_program('input.21.txt')

_16 = __import__('2018_16')
_19 = __import__('2018_19')


def program_runner(program: [str]):
    instruction_pointer_register = 2
    registers = [0] * 6
    instruction_pointer = 0

    while instruction_pointer < len(program) and instruction_pointer >= 0:
        instruction = program[instruction_pointer]

        registers[instruction_pointer_register] = instruction_pointer
        registers = _16.opcodes[instruction[0]](registers, instruction)

        if instruction_pointer == 28:
            yield registers[3]

        instruction_pointer = registers[instruction_pointer_register]
        instruction_pointer += 1


def solution_first_part(program: [str]):
    generator = program_runner(program)
    return next(generator)


#The input taken from: https://adventofcode.com/2018/day/21/input
program = _19.input_to_program('''<input>'''.splitlines())


def find_last_in_cycle(file_name) -> int:
    been = set()
    last = None

    # I transcripe input to language which allow for goto, output of it (D register for every 28-th instruction) is input in this case
    for line in open(file_name, 'r'):
        tmp = int(line)
        if tmp in been:
            return last 

        last = tmp
        been.add(tmp)


print('Solution for the first part:', solution_first_part(program))
print('Solution for the second part:', find_last_in_cycle('result_of_c_program'))
