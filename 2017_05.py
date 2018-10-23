def count_jumps(memory):
    index = 0
    memory_lenght = len(memory)
    jump_count = 0

    while index < memory_lenght:
        jump = memory[index]
        memory[index] += 1
        index += jump
        jump_count += 1

    return jump_count

assert count_jumps([0, 3, 0, 1, -3]) == 5

def read_memory_file(file_name) -> [int]:
    with open(file_name) as file:
        return [int(line.rstrip('\n')) for line in file]

# The file creaded based from https://adventofcode.com/2017/day/5/input
print(count_jumps(read_memory_file('memory.txt')))
