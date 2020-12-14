MASK_SIZE = 36


def load_input_file(file_name: str) -> [str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


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
                for m, v in zip(
                    mask,
                    '{0:b}'.format(value).zfill(MASK_SIZE))),
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
