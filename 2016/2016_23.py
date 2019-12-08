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


def cpu(program, registries):

    def value_or_registry(registries, value):
        return registries[value] if value in registries.keys() else value

    def cpy(index, registries, x, y):
        if y in registries:
            registries[y] = value_or_registry(registries, x)
        return None

    def inc(index, registries, x, _):
        registries[x] += 1
        return None

    def dec(index, registries, x, _):
        registries[x] -= 1
        return None

    def jnz(index, registries, x, y):
        return value_or_registry(registries, y) if value_or_registry(registries, x) != 0 else None

    def tgl(index, registries, x, _):
        new_index = value_or_registry(registries, x) + index
        if new_index >= len(program) or new_index < 0:
            return None

        command, a, b = program[new_index]
        if command in ['dec', 'inc']:
            program[new_index] = ('dec' if command == 'inc' else 'inc', a, b)
        elif command in ['jnz', 'cpy']:
            program[new_index] = ('cpy' if command == 'jnz' else 'jnz', a, b)
        elif command == 'tgl':
            program[new_index] = ('inc', a, b)

        return None


    INSTRUCTIONS = {
        'cpy': cpy,
        'inc': inc,
        'dec': dec,
        'jnz': jnz,
        'tgl': tgl
    }

    index = 0
    while index < len(program):
        command, first, second = program[index]
        jump = INSTRUCTIONS[command](index, registries, first, second)
        index += jump if jump != None else 1

    return registries


def solution_for_first_part(program_text):
    program = list(parse_input(program_text))
    registries = build_registers()
    registries['a'] = 7
    registries = cpu(program, registries)

    return registries['a']


test_program = '''cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a'''.splitlines()

assert solution_for_first_part(test_program) == 3

# The input is taken from: https://adventofcode.com/2016/day/23/input
program = load_input_file('input.23.txt')
print("Solution for the first part:", solution_for_first_part(program))
