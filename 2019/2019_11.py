END_OPTCODE = 99
BLACK = 0
WHITE = 1


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
            return outside, index, memory, relative_base

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


def run_painting_program(memory, initial_state = None):
    memory = {i:v for i, v in enumerate(memory)}
    index, relative_base = 0, 0
    panels = initial_state or {}
    x, y, facing = 0, 0, 0

    while True:
        output, index, memory, relative_base = run_program(memory, [panels.get((x, y), BLACK)], index, relative_base)
        if memory[index] == END_OPTCODE:
            break

        panels[(x, y)] = output
        output, index, memory, relative_base = run_program(memory, [panels.get((x, y), BLACK)], index, relative_base)
        if memory[index] == END_OPTCODE:
            break

        if output == 0:
            facing = (facing + 1) % 4
        else:
            facing = (facing - 1) % 4
        
        if facing == 0:
            y -= 1
        elif facing == 1:
            x -= 1
        elif facing == 2:
            y += 1
        elif facing == 3:
            x += 1

    return panels


def solution_for_first_part(task_input):
    panels = run_painting_program(task_input)
    return len(panels)


# The input is taken from: https://adventofcode.com/2019/day/11/input
task_input = load_input_file('input.11.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input):
    panels = run_painting_program(task_input, {(0,0): WHITE})

    coorinates_list = panels.keys()
    x_coorinates = [x for x, _ in coorinates_list]
    y_coorinates = [y for _, y in coorinates_list]

    for y in range(min(y_coorinates), max(y_coorinates) + 1):
        for x in range(min(x_coorinates), max(x_coorinates) + 1):
            print('#' if panels.get((x, y), BLACK) == WHITE else '.', end='')
        
        print()


print("Solution for the second part:")
solution_for_second_part(task_input)
