def count_jumps(memory, jump_policy):
    index = 0
    memory_lenght = len(memory)
    jump_count = 0

    while index < memory_lenght:
        offset = memory[index]
        memory[index] = jump_policy(memory[index])
        index += offset
        jump_count += 1

    return jump_count


def count_jumps_a(memory):
    return count_jumps(memory, lambda x: x + 1)


def count_jumps_b(memory):
    return count_jumps(memory, lambda x: x - 1 if x >= 3 else x + 1)


def read_memory_file(file_name) -> [int]:
    with open(file_name) as file:
        return [int(line.rstrip('\n')) for line in file]

example_memory = [0, 3, 0, 1, -3]

assert count_jumps_a(example_memory) == 5
assert count_jumps_b(example_memory) == 10

# The file creaded based on https://adventofcode.com/2017/day/5/input
memory = read_memory_file('memory.txt')

print(count_jumps_a(memory))
print(count_jumps_b(memory))  # long time of executing
