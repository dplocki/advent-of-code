def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: [str]):
    for line in task_input:
        instruction, value = line.split(' ')
        yield instruction, int(value)


def run_program(program: [str]) -> int:
    instruction_number = len(program)
    visited_instructions = set()
    accumulator = 0
    index = 0

    while not index in visited_instructions:
        if index >= instruction_number:
            return accumulator, True

        instruction, value = program[index]
        visited_instructions.add(index)

        if instruction == 'acc':
            accumulator += value
            index += 1
        elif instruction == 'jmp':
            index += value
        elif instruction == 'nop':
            index += 1
        else:
            raise Exception('Unknown instruction')

    return accumulator, False


def solution_for_first_part(task_input: [str]) -> int:
    program = list(parse(task_input))
    return run_program(program)[0]

example_input = '''nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6'''.splitlines()

assert solution_for_first_part(example_input) == 5

# The input is taken from: https://adventofcode.com/2020/day/8/input
task_input = list(load_input_file('input.08.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: [str]):
    original_program = list(parse(task_input))

    for index, line in enumerate(original_program):
        instruction, value = line
        if instruction == 'acc':
            continue

        program = original_program.copy()
        program[index] = 'nop' if instruction == 'jmp' else 'jmp', value

        accumulator, has_index_cross_program = run_program(program)
        if has_index_cross_program:
            return accumulator


assert solution_for_second_part(example_input) == 8
print("Solution for the second part:", solution_for_second_part(task_input))
