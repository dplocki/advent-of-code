def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse_input(input: [str]):

    def as_number_if_number(value):
        return int(value) if value.lstrip('-').isnumeric() else value

    for line in input:
        tokens = line.split(' ')
        yield (
                tokens[0],
                as_number_if_number(tokens[1]),
                as_number_if_number(tokens[2]) if len(tokens) > 2 else None
            )

def value_or_registry(registries, value):
    return registries[value] if value in registries.keys() else value

def cpy(registries, x, y):
    registries[y] = value_or_registry(registries, x)
    return None

def inc(registries, x, y):
    registries[x] += 1
    return None

def dec(registries, x, y):
    registries[x] -= 1
    return None

def jnz(registries, x, y):
    return y if value_or_registry(registries, x) != 0 else None

def cpu(program, registries):
    INSTRUCTIONS = {
        'cpy': cpy,
        'inc': inc,
        'dec': dec,
        'jnz': jnz
    }

    index = 0
    while index < len(program):
        command, first, second = program[index]
        jump = INSTRUCTIONS[command](registries, first, second)
        index += jump if jump != None else 1

    return registries



def solution_for_first_part(program):
    registries = cpu(program, { l: 0 for l in 'abcd' })
    return registries['a']


# The input is taken from: https://adventofcode.com/2016/day/12/input
program = [instruction for instruction in parse_input(load_input_file('input.12.txt'))]
print("Solution for the first part:", solution_for_first_part(program))
