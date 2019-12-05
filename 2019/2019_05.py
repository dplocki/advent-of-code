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
            raise f'Uknown mode: {mode}'

    def to_memory(memory, paramater, value):
        index, mode = paramater

        if mode == 0:
            memory[memory[index]] = value
        elif mode == 1:
            memory[index] = value
        else:
            raise f'Uknown mode: {mode}'

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

        else:
            raise f'Unknown opcode: "{cmd}"'


# The input is taken from: https://adventofcode.com/2019/day/5/input
memory_input = load_input_file('input.05.txt')
print("Solution for the first part:", run_program(memory_input, 1))
