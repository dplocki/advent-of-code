MASK_SIZE = 36


def load_input_file(file_name: str) -> [str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def to_bits(value: str, size: int=MASK_SIZE) -> [str]:
    return '{0:b}'.format(value).zfill(size)


def parse(task_input: [str]) -> [tuple]:
    mask = None
    for line in task_input:
        left, right = line.split(' = ')
        if left == 'mask':
            mask = right
        else:
            yield mask, int(left[4:-1]), int(right)


def solution_for_first_part(task_input: [str]) -> int:
    memory = {}
    for mask, adress, value in parse(task_input):
        memory[adress] = int(
            ''.join(
                m if m in '01' else v
                for m, v in zip(mask, to_bits(value))),
            2)

    return sum(memory.values())


example_input = '''mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0'''.splitlines()

assert solution_for_first_part(example_input) == 165

# The input is taken from: https://adventofcode.com/2020/day/14/input
task_input = list(load_input_file('input.14.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: [tuple]) -> int:

    def apply_mask(mask, value):
        return (
            m if m in 'X1' else v
            for m, v in zip(mask, to_bits(value)))


    def replace_empty_bits(pattern: [str], value: [str]) -> [str]:
        result = pattern.copy()

        x = 0
        for i, c in enumerate(result):
            if c == 'X':
                result[i] = combination_as_bits[x]
                x += 1

        return result


    memory = {}    
    for mask, adress, value in list(parse(task_input)):
        pattern = list(apply_mask(mask, adress))
        x_number = pattern.count('X')

        for combination in range(2 ** x_number):
            combination_as_bits = list(to_bits(combination, x_number))
            new_address = replace_empty_bits(pattern, combination_as_bits)
            memory[int(''.join(new_address), 2)] = value

    return sum(memory.values())


example_input_part2 = '''mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1'''.splitlines()

assert solution_for_second_part(example_input_part2) == 208
print("Solution for the second part:", solution_for_second_part(task_input))
