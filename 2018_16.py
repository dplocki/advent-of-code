import re


OPCODE = 0
A = 1
B = 2
C = 3


def addr(registers, instructions):
    result = registers[:]
    result[instructions[C]] = registers[instructions[A]] + registers[instructions[B]]
    return result


def addi(registers, instructions):
    result = registers[:]
    result[instructions[C]] = registers[instructions[A]] + instructions[B]
    return result


def mulr(registers, instructions):
    result = registers[:]
    result[instructions[C]] = registers[instructions[A]] * registers[instructions[B]]
    return result


def muli(registers, instructions):
    result = registers[:]
    result[instructions[C]] = registers[instructions[A]] * instructions[B]
    return result


def banr(registers, instructions):
    result = registers[:]
    result[instructions[C]] = registers[instructions[A]] & registers[instructions[B]]
    return result


def bani(registers, instructions):
    result = registers[:]
    result[instructions[C]] = registers[instructions[A]] & instructions[B]
    return result


def borr(registers, instructions):
    result = registers[:]
    result[instructions[C]] = registers[instructions[A]] | registers[instructions[B]]
    return result


def bori(registers, instructions):
    result = registers[:]
    result[instructions[C]] = registers[instructions[A]] | instructions[B]
    return result


def setr(registers, instructions):
    result = registers[:]
    result[instructions[C]] = registers[instructions[A]]
    return result


def seti(registers, instructions):
    result = registers[:]
    result[instructions[C]] = instructions[A]
    return result


def gtir(registers, instructions):
    result = registers[:]
    result[instructions[C]] = 1 if instructions[A] > registers[instructions[B]] else 0
    return result


def gtri(registers, instructions):
    result = registers[:]
    result[instructions[C]] = 1 if registers[instructions[A]] > instructions[B] else 0
    return result


def gtrr(registers, instructions):
    result = registers[:]
    result[instructions[C]] = 1 if registers[instructions[A]] > registers[instructions[B]] else 0
    return result


def eqir(registers, instructions):
    result = registers[:]
    result[instructions[C]] = 1 if instructions[A] == registers[instructions[B]] else 0
    return result


def eqri(registers, instructions):
    result = registers[:]
    result[instructions[C]] = 1 if registers[instructions[A]] == instructions[B] else 0
    return result


def eqrr(registers, instructions):
    result = registers[:]
    result[instructions[C]] = 1 if registers[instructions[A]] == registers[instructions[B]] else 0
    return result


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


def checking_sample(registers_before, instruction, registers_after) -> int:
    behave = 0
    for _, opcode in opcodes.items():
        recived_registers_after = opcode(registers_before, instruction)
        if recived_registers_after == registers_after:
            behave +=1
    
    return behave


def parse_input_file(file_name):
    with open(file_name, 'r') as content_file:
        content = content_file.read()
        re.findall(r'Before: \[(\d), (\d), (\d), (\d)\]\n(\d+) (\d+) (\d+) (\d+)\nAfter:  \[(\d), (\d), (\d), (\d)\]', content,  re.MULTILINE)

        for match in re.finditer(r'Before: \[(\d), (\d), (\d), (\d)\]\n(\d+) (\d+) (\d+) (\d+)\nAfter:  \[(\d), (\d), (\d), (\d)\]', content,  re.MULTILINE):
            yield [int(match.group(i)) for i in range(1, 5)], [int(match.group(i)) for i in range(5, 9)], [int(match.group(i)) for i in range(9, 13)]


def how_many_samples_match_3_or_more(samples: []):
    result = 0

    for before, instruction, after in samples:
        matching = checking_sample(before, instruction, after)
        if matching >= 3:
            result += 1

    return result


assert checking_sample([3, 2, 1, 1], [9, 2, 1, 2], [3, 2, 2, 1]) == 3

# Input taken from: https://adventofcode.com/2018/day/16/input (only first part)
print("Solution for first part:", how_many_samples_match_3_or_more(parse_input_file('input.first_part.txt')))

