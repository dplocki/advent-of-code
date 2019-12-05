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
    outside = [initial_input]

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


# The input is taken from: https://adventofcode.com/2019/day/5/input
memory_input = load_input_file('input.05.txt')
print("Solution for the first part:", run_program(memory_input[:], 1))

assert run_program([3,9,8,9,10,9,4,9,99,-1,8], 8) == 1
assert run_program([3,9,8,9,10,9,4,9,99,-1,8], 7) == 0

assert run_program([3,9,7,9,10,9,4,9,99,-1,8], 7) == 1
assert run_program([3,9,7,9,10,9,4,9,99,-1,8], 8) == 0

assert run_program([3,3,1108,-1,8,3,4,3,99], 8) == 1
assert run_program([3,3,1108,-1,8,3,4,3,99], 7) == 0

assert run_program([3,3,1107,-1,8,3,4,3,99], 7) == 1
assert run_program([3,3,1107,-1,8,3,4,3,99], 17) == 0

assert run_program([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 0) == 0
assert run_program([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 1) == 1

assert run_program([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 0) == 0
assert run_program([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 1) == 1

larger_example_input = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
assert run_program(larger_example_input[:], 7) == 999
assert run_program(larger_example_input[:], 8) == 1000
assert run_program(larger_example_input[:], 9) == 1001

print("Solution for the second part:", run_program(memory_input[:], 5))
