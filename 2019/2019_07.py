import itertools


END_OPTCODE = 99


def load_input_file(file_name):
    with open(file_name) as file:
        return [int(x) for x in file.read().split(',')]


def run_program(memory, initial_input, index=0):

    def from_memory(memory, paramater):
        index, mode = paramater

        if mode == 0:
            return memory[memory[index]]
        elif mode == 1:
            return memory[index]
        else:
            raise Exception(f'Uknown mode: {mode}')

    def to_memory(memory, paramater, value):
        index, mode = paramater

        if mode == 0:
            memory[memory[index]] = value
        elif mode == 1:
            memory[index] = value
        else:
            raise Exception(f'Uknown mode: {mode}')

    outside = initial_input

    while True:
        cmd = memory[index]

        optcode = cmd % 100
        first_parameter = (index + 1, (cmd // 100) % 10)
        second_parameter = (index + 2, (cmd // 1000) % 10)
        third_parameter = (index + 3, (cmd // 10000) % 10)

        if optcode == END_OPTCODE:
            return outside, index, memory

        # Calculation
        elif optcode == 1: # adding
            to_memory(
                memory,
                third_parameter,
                from_memory(memory, first_parameter) + from_memory(memory, second_parameter)
            )
            index += 4

        elif optcode == 2: # multiplication
            to_memory(
                memory,
                third_parameter, 
                from_memory(memory, first_parameter) * from_memory(memory, second_parameter)
            )
            index += 4
        
        # I/O operations
        elif optcode == 3: # to output
            to_memory(memory, first_parameter, outside.pop(0))
            index += 2

        elif optcode == 4: # from input
            outside.append(from_memory(memory, first_parameter))
            index += 2
            return outside, index, memory

        # Jumps
        elif optcode == 5: # jump-if-true
            index = from_memory(memory, second_parameter) if from_memory(memory, first_parameter) != 0 else index + 3
        
        elif optcode == 6: # jump-if-false
            index = from_memory(memory, second_parameter) if from_memory(memory, first_parameter) == 0 else index + 3

        # Save in memory operations
        elif optcode == 7: # less than
            to_memory(memory, third_parameter, 1 if from_memory(memory, first_parameter) < from_memory(memory, second_parameter) else 0)
            index += 4

        elif optcode == 8: # equals
            to_memory(memory, third_parameter, 1 if from_memory(memory, first_parameter) == from_memory(memory, second_parameter) else 0)
            index += 4

        else:
            raise Exception(f'Unknown opcode: "{cmd}"')


def run_program_to_finished(memory, initial_input, index=0): 
    while memory[index] != END_OPTCODE:
        output, index, memory = run_program(memory, initial_input, index)

    return output.pop()


def solution_for_first_part(task_input: [int]):

    def thruster_generator(task_input):
        for sample in itertools.permutations(range(5)):
            memory = [task_input[:] for _ in range(5)]

            outside = 0
            for i in range(5):
                outside = run_program_to_finished(memory[i], [sample[i], outside])

            yield outside

    return max(thruster_generator(task_input))


assert solution_for_first_part([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]) == 43210
assert solution_for_first_part([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]) == 54321
assert solution_for_first_part([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]) == 65210


# The input is taken from: https://adventofcode.com/2019/day/7/input
memory_input = load_input_file('input.07.txt')
print("Solution for the first part:", solution_for_first_part(memory_input))


def solution_for_second_part(task_input: [int]):

    def thruster_generator(task_input):
        for sample in itertools.permutations(range(5, 9 + 1)):
            memories = [task_input[:] for i in range(5)]
            indexes = [0 for i in range(5)]
            outside = [0]

            for i in range(5):
                outside, indexes[i], memories[i] = run_program(memories[i], [sample[i], outside[0]], indexes[i])

            while True:
                for i in range(5):
                    outside, indexes[i], memories[i] = run_program(memories[i], outside, indexes[i])

                if memories[4][indexes[4]] == END_OPTCODE:
                    yield outside[0]
                    break


    return max(thruster_generator(task_input))


assert solution_for_second_part([
        3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
        27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
    ]) == 139629729
assert solution_for_second_part([
        3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
        -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
        53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10
    ]) == 18216

print("Solution for the second part:", solution_for_second_part(memory_input))
