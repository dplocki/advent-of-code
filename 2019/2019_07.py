import itertools


def load_input_file(file_name):
    with open(file_name) as file:
        return [int(x) for x in file.read().split(',')]


def run_program(memory, initial_input):

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

    index = 0
    outside = initial_input

    while True:
        cmd = memory[index]

        optcode = cmd % 100
        first_parameter = (index + 1, (cmd // 100) % 10)
        second_parameter = (index + 2, (cmd // 1000) % 10)
        third_parameter = (index + 3, (cmd // 10000) % 10)

        if optcode == 99:
            return outside.pop()

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
   

def solution_for_first_part(task_input: [int]):

    def thruster_generator():
        for sample in itertools.permutations(range(5)):
            memory = [task_input[:] for _ in range(5)]

            outside = 0
            for i in range(5):
                outside = run_program(memory[i], [sample[i], outside])

            yield outside

    return max(thruster_generator())


assert solution_for_first_part([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]) == 43210
assert solution_for_first_part([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]) == 54321
assert solution_for_first_part([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]) == 65210


# The input is taken from: https://adventofcode.com/2019/day/7/input
memory_input = load_input_file('input.07.txt')
print("Solution for the first part:", solution_for_first_part(memory_input))
