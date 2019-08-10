import re


def parsing(program_lines):
	pattern = re.compile(r'([a-z]{3}) ([a|b])?(?:, )?([-|+]\d+)?')
	for line in program_lines:
		groups = pattern.match(line)
		yield groups[1], groups[2], int(groups[3]) if groups[3] else 0


def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def run_program_return_registers_after(program: [str], init_registers = None) -> {}:
	if init_registers == None:
		registers = { 'a': 0, 'b': 0 }
	else:
		registers = init_registers

	max_length = len(program)
	index = 0
	while max_length > index:
		instruction, register, offset = program[index]

		if instruction == 'hlf':
			registers[register] //= 2
			index += 1
		elif instruction == 'tpl':
			registers[register] *= 3
			index += 1
		elif instruction == 'inc':
			registers[register] += 1
			index += 1
		elif instruction == 'jmp':
			index += offset
		elif instruction == 'jie':
			index += offset if registers[register] % 2 == 0 else 1
		elif instruction == 'jio':
			index += offset if registers[register] == 1 else 1
		else:
			raise Exception('Unknown instruction: ' + instruction)

	return registers


def solution_for_first_part(program: [str]) -> int:
	registers = run_program_return_registers_after(program)

	return registers['b']


def solution_for_second_part(program: [str]) -> int:
	registers = run_program_return_registers_after(program, {'a': 1, 'b': 0})

	return registers['b']


# The input is taken from: https://adventofcode.com/2015/day/23/input
program = list(parsing(load_input_file('input.23.txt')))

print("Solution for the first part:", solution_for_first_part(program))
print("Solution for the second part:", solution_for_second_part(program))
