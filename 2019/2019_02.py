def load_input_file(file_name):
    with open(file_name) as file:
        return file.read()


def run_program(memory):
    index = 0
    while True:
        cmd = memory[index]

        if cmd == 99:
            return memory[0]
        elif cmd == 1:
            memory[memory[index + 3]] = memory[memory[index + 1]] + memory[memory[index + 2]]
        elif cmd == 2: 
            memory[memory[index + 3]] = memory[memory[index + 1]] * memory[memory[index + 2]]
        else:
            raise f'Unknown opcode: "{cmd}"'

        index += 4


def solution_for_the_first_part(memory_input):
    memory = memory_input.copy()
    memory[1] = 12
    memory[2] = 2

    return run_program(memory)


# The input is taken from: https://adventofcode.com/2019/day/2/input
memory_input = [int(x) for x in load_input_file('input.02.txt').split(',')]

print("Solution for the first part:", solution_for_the_first_part(memory_input))


def solution_for_the_second_part(memory_input):
    for x in range(0, 100):
        for y in range(0, 100):
            memory = memory_input.copy()
            memory[1] = x
            memory[2] = y

            if run_program(memory) == 19690720:
                return x * 100 + y


print("Solution for the second part:", solution_for_the_second_part(memory_input))
