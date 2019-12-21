import itertools


END_OPTCODE = 99


def load_input_file(file_name):
    with open(file_name) as file:
        return [int(x) for x in file.read().split(',')]


def run_program(memory: {}, outside, index=0, relative_base=0) -> []:

    def from_memory(memory, paramater, relative_base):
        index, mode = paramater
        
        # position mode
        if mode == 0:
            return memory.get(memory[index], 0)
        # immediate mode
        elif mode == 1:
            return memory.get(index, 0)
        # relative mode
        elif mode == 2:
            return memory.get(relative_base + memory[index], 0)
        else:
            raise Exception(f'Uknown mode: {mode}')

    def to_memory(memory, paramater, value, relative_base):
        index, mode = paramater

        new_index = None
        # position mode
        if mode == 0:
            new_index = memory[index]
        # immediate mode
        elif mode == 1:
            new_index = index
        # relative mode
        elif mode == 2:
            new_index = relative_base + memory[index]
        else:
            raise Exception(f'Uknown mode: {mode}')

        memory[new_index] = value

    while True:
        cmd = memory[index]

        optcode = cmd % 100
        first_parameter = (index + 1, (cmd // 100) % 10)
        second_parameter = (index + 2, (cmd // 1000) % 10)
        third_parameter = (index + 3, (cmd // 10000) % 10)

        if optcode == END_OPTCODE:
            return None, index, memory, relative_base

        # Calculation
        elif optcode == 1: # adding
            to_memory(
                memory,
                third_parameter,
                from_memory(memory, first_parameter, relative_base) + from_memory(memory, second_parameter, relative_base),
                relative_base
            )
            index += 4

        elif optcode == 2: # multiplication
            to_memory(
                memory,
                third_parameter, 
                from_memory(memory, first_parameter, relative_base) * from_memory(memory, second_parameter, relative_base),
                relative_base
            )
            index += 4
        
        # I/O operations
        elif optcode == 3:
            to_memory(memory, first_parameter, outside.pop(0), relative_base)
            index += 2

        elif optcode == 4:
            index += 2
            return from_memory(memory, first_parameter, relative_base), index, memory, relative_base

        # Jumps
        elif optcode == 5: # jump-if-true
            index = from_memory(memory, second_parameter, relative_base) if from_memory(memory, first_parameter, relative_base) != 0 else index + 3
        
        elif optcode == 6: # jump-if-false
            index = from_memory(memory, second_parameter, relative_base) if from_memory(memory, first_parameter, relative_base) == 0 else index + 3

        # Save in memory operations
        elif optcode == 7: # less than
            to_memory(
                memory,
                third_parameter,
                1 if from_memory(memory, first_parameter, relative_base) < from_memory(memory, second_parameter, relative_base) else 0,
                relative_base
            )
            index += 4

        elif optcode == 8: # equals
            to_memory(
                memory,
                third_parameter,
                1 if from_memory(memory, first_parameter, relative_base) == from_memory(memory, second_parameter, relative_base) else 0, relative_base
            )
            index += 4

        # Adjust the relative base
        elif optcode == 9:
            relative_base += from_memory(memory, first_parameter, relative_base)
            index += 2

        else:
            raise Exception(f'Unknown opcode: "{cmd}"')

    
def run_program_to_end(memory: {}, program_input):
    index, relative_base = 0, 0
    while memory[index] != END_OPTCODE:
        output, index, memory, relative_base = run_program(memory, program_input, index, relative_base)
        yield output


def solution_for_first_part(task_input):
    script = '''OR A J
AND B J
AND C J
NOT J J
AND D J'''

    memory = {i:v for i, v in enumerate(task_input)}
    for i in run_program_to_end(memory, [ord(c) for c in script + '\nWALK\n']):
        if i > 0x10FFFF:
            return i


# The input is taken from: https://adventofcode.com/2019/day/21/input
memory = list(load_input_file('input.21.txt'))
print("Solution for the first part:", solution_for_first_part(memory))
