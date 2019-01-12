import re


def file_to_input_list(file_name):
    with open(file_name) as file:
        return file.read()


def parse_initial(lines):
    match = re.match(r'Begin in state (.)\.\nPerform a diagnostic checksum after (\d+) steps\.', lines, re.MULTILINE)
    return match[1], int(match[2])


def parse_program(lines):


    def read_program(lines):
        for match in re.finditer(r'''In state (.):
  If the current value is (\d):
    - Write the value (\d)\.
    - Move one slot to the (left|right)\.
    - Continue with state (.)\.
  If the current value is (\d):
    - Write the value (\d)\.
    - Move one slot to the (left|right)\.
    - Continue with state (.)\.''', lines, re.MULTILINE):
            yield match[1], int(match[2]), int(match[3]), match[4], match[5]
            yield match[1], int(match[6]), int(match[7]), match[8], match[9]

    program = {}
    for current_state, current_value, new_value, move, new_state in read_program(input_text):
        sub_program = program.get(current_state, {})
        sub_program[current_value] = (new_value, 1 if move == 'right' else -1, new_state)
        program[current_state] = sub_program

    return program  


def run_program(program: {}, init: str, end: int):
    memory = {}
    index = 0
    state = init

    for _ in range(end):
        sub_program = program[state][memory.get(index, 0)]

        memory[index] = sub_program[0]
        index += sub_program[1]
        state = sub_program[2]

    return list(memory.values()).count(1)


# The input taken from: https://adventofcode.com/2017/day/25/input
input_text = file_to_input_list('input.25.txt')

print('Solution for the first part:', run_program(parse_program(input_text), *parse_initial(input_text)))
