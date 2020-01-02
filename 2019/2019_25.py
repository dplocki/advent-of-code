from itertools import combinations
import re


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
            if not outside:
                return None, index, memory, relative_base

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


def generete_backpack_combination(all_items: set):


    def combination(all_items):
        for i in range(len(all_items) -1, 0, -1):
            yield from [set(c) for c in combinations(all_items, i)]


    current_backpack = all_items.copy()
    for c in combination(all_items):
        to_drop = current_backpack.difference(c)
        to_take = c.difference(current_backpack)

        yield ''.join([f'drop {d}\n' for d in to_drop]) + ''.join([f'take {t}\n' for t in to_take]) + 'north\n'
        current_backpack = c


def run_program_to_end(task_input: {}, instructions: [str]=None):
    memory = {i:v for i, v in enumerate(task_input)}
    index, relative_base = 0, 0
    program_input = [ord(c) for c in instructions] if instructions else []
    program_output = []
    backpack = set(re.compile(r'(?<=take )[a-z ]+(?=\n)').findall(instructions or '', re.MULTILINE))
    backpack_generator = generete_backpack_combination(backpack)

    while memory[index] != END_OPTCODE:
        output, index, memory, relative_base = run_program(memory, program_input, index, relative_base)
        if output == None:
            user_input = input() + '\n'
            if user_input == 'find correct combination\n':
                user_input = ''.join(backpack_generator)

            # with open("instructions.txt", "a") as myfile:
            #     myfile.write(user_input)

            program_input = [ord(c) for c in user_input]
        else:
            program_output.append(output)
            if output == 10:
                line = ''.join([chr(i) for i in program_output])
                program_output = []
                print(line)


# The input is taken from: https://adventofcode.com/2019/day/25/input
task_input = load_input_file('input.25.txt')
# Walk around ship, gather all pickup-able items, walk into security check
run_program_to_end(task_input)
