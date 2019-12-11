CHECKING_PATERN_SIZE = 10


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


def build_registers():
    return { l: 0 for l in 'abcd' }


def cpu(program, registries, index = 0):

    def value_or_registry(registries, value):
        return registries[value] if value in registries.keys() else value

    def cpy(index, registries, x, y):
        if y in registries:
            registries[y] = value_or_registry(registries, x)
        return None, None

    def inc(index, registries, x, _):
        registries[x] += 1
        return None, None

    def dec(index, registries, x, _):
        registries[x] -= 1
        return None, None

    def jnz(index, registries, x, y):
        return value_or_registry(registries, y) if value_or_registry(registries, x) != 0 else None, None

    def out(index, registries, x, y):
        return None, value_or_registry(registries, x)


    INSTRUCTIONS = {
        'cpy': cpy,
        'inc': inc,
        'dec': dec,
        'jnz': jnz,
        'out': out
    }

    while index < len(program):
        command, first, second = program[index]
        jump, out_value = INSTRUCTIONS[command](index, registries, first, second)
        if out_value != None:
            yield out_value
            out_value = None

        index += jump if jump != None else 1


def solution_for_first_part(program_text):

    def check_value(program, patern, a_value):
        registries = build_registers()
        registries['a'] = a_value
        
        for f, s in zip(cpu(program, registries), patern):
            if f != s:
                return False

        return True


    program = list(parse_input(program_text))
    patern = [i % 2 for i in range(CHECKING_PATERN_SIZE)]

    a_value = 0
    while True:
        if check_value(program, patern, a_value):
            return a_value

        a_value += 1


# The input is taken from: https://adventofcode.com/2016/day/25/input
print("Solution for the first part:", solution_for_first_part(load_input_file('input.25.txt')))
