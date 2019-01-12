import re


OPT_CODES_NUMBER = 16
REGISTER_NUMBER = 4
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
    matching = set()

    for op_name, opcode in opcodes.items():
        recived_registers_after = opcode(registers_before, instruction)
        if recived_registers_after == registers_after:
            matching.add(op_name)
    
    return matching


def parse_input_file(file_name):
    with open(file_name, 'r') as content_file:
        content = content_file.read()

        for match in re.finditer(r'Before: \[(\d), (\d), (\d), (\d)\]\n(\d+) (\d+) (\d+) (\d+)\nAfter:  \[(\d), (\d), (\d), (\d)\]', content,  re.MULTILINE):
            yield [int(match.group(i)) for i in range(1, 5)], [int(match.group(i)) for i in range(5, 9)], [int(match.group(i)) for i in range(9, 13)]


def how_many_samples_match_3_or_more(samples: []):
    result = 0

    for before, instruction, after in samples:
        matching = checking_sample(before, instruction, after)
        if len(matching) >= 3:
            result += 1

    return result


def samples_to_opt_codes_candidates(samples: []):
    number_to_ops = { i: set() for i in range(OPT_CODES_NUMBER) }

    for before, instruction, after in samples:
        opt_code = instruction[0]

        matching = checking_sample(before, instruction, after)
        number_to_ops[opt_code].update(matching)

    return number_to_ops


def translate_opt_codes(samples: []):
    opt_code_candidates = samples_to_opt_codes_candidates(samples)
    result = {}

    while len(result) < OPT_CODES_NUMBER:
        # Find all with only one candidates
        singulars = [(opt_code, list(candidates)[0]) for opt_code, candidates in opt_code_candidates.items() if len(candidates) == 1]
        
        for new_recognise_optcode, recognise_name in singulars:
            result[new_recognise_optcode] = recognise_name

            # Remove those from others list
            for unknown_optcode, _ in opt_code_candidates.items():
                opt_code_candidates[unknown_optcode].discard(recognise_name)

    return result


def parse_program_file(file_name: str):
    pattern = re.compile(r'(\d+) (\d+) (\d+) (\d+)')
    new_line_count = 0
    program_part_of_file = False

    with open(file_name, 'r') as file:
        for line in file:
            if program_part_of_file:
                match = pattern.match(line.strip())
                yield [int(match[i]) for i in range(1, 5)]
            else:
                if line == '\n':
                    new_line_count += 1
                else:
                    new_line_count = 0

                if new_line_count > 2:
                    program_part_of_file = True


def run_program(opt_codes_to_instruction, program: [str]):
    registers = [0] * REGISTER_NUMBER

    for instruction in program:
        registers = opcodes[opt_codes_to_instruction[instruction[0]]](registers, instruction)

    return registers


if __name__ == "__main__":
    assert len(checking_sample([3, 2, 1, 1], [9, 2, 1, 2], [3, 2, 2, 1])) == 3

    # Input taken from: https://adventofcode.com/2018/day/16/input
    print("Solution for first part:", how_many_samples_match_3_or_more(parse_input_file('input.16.txt')))

    program = parse_program_file('input.16.txt')
    print("Solution for second part:", run_program(translate_opt_codes(parse_input_file('input.16.txt')), program)[0])
