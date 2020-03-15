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
            if outside:
                to_memory(memory, first_parameter, outside.pop(0), relative_base)
                index += 2
            else:
                return None, index, memory, relative_base

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


def run_network_return_nant_y(memory: dict) -> [int]:
    number_program = 50
    program_input = [[network_address] for network_address in range(number_program)]
    program_states = [(0, {i:v for i, v in enumerate(task_input)}, 0) for _ in range(number_program)]
    nant = None

    while True:
        for n in range(number_program):
            index, memory, relative_base = program_states[n]

            if not program_input[n]:
                program_input[n].append(-1)

            output, index, memory, relative_base = run_program(memory, program_input[n], index, relative_base)
            if output != None:
                where = output

                output, index, memory, relative_base = run_program(memory, program_input[n], index, relative_base)
                x = output

                output, index, memory, relative_base = run_program(memory, program_input[n], index, relative_base)
                y = output

                if where == 255:
                    nant = x, y
                else:
                    program_input[where].append(x)
                    program_input[where].append(y)

            program_states[n] = index, memory, relative_base

        if nant != None and not any(program_input):
            program_input[0].extend(nant)
            yield nant[1]


def solution_for_first_part(task_input: dict) -> int:
    return next(run_network_return_nant_y(task_input))


# The input is taken from: https://adventofcode.com/2019/day/23/input
task_input = load_input_file('input.23.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: dict) -> int:
    y_nant_set = set()

    for y_nant in run_network_return_nant_y(task_input):
        if y_nant in y_nant_set:
            return y_nant
        else:
            y_nant_set.add(y_nant)


print("Solution for the second part:", solution_for_second_part(task_input))
