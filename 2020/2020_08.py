def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def solution_for_first_part(task_input: []):

    def parse(task_input: [str]):
        for line in task_input:
            instruction, value = line.split(' ')
            yield instruction, int(value)


    program = { v:k for v, k in enumerate(parse(task_input)) }
    visited_instructions = set()
    accumulator = 0
    index = 0

    while not index in visited_instructions:
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

    return accumulator


assert solution_for_first_part('''nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6'''.splitlines()) == 5

# The input is taken from: https://adventofcode.com/2020/day/8/input
task_input = load_input_file('input.08.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
