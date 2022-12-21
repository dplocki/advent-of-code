from typing import Generator, Iterable


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]):
    for line in task_input:
        monkey_name, monkey_instructions = line.split(': ')
        monkey_instructions = monkey_instructions.split(' ')
        yield monkey_name, int(monkey_instructions[0]) if len(monkey_instructions) == 1 else tuple(monkey_instructions)


def solution_for_first_part(task_input: Iterable[str]) -> int:
    monkeys_instructions = list(parse(task_input))
    result = {}
    while True:
        for monkey_name, monkey_yells in monkeys_instructions:
            if monkey_name in result:
                continue

            if isinstance(monkey_yells, tuple):
                first_monkey, operation, second_monkey = monkey_yells
                
                if first_monkey in result and second_monkey in result:
                    if operation == '+':
                        result[monkey_name] = result[first_monkey] + result[second_monkey]
                    elif operation == '*':
                        result[monkey_name] = result[first_monkey] * result[second_monkey]
                    elif operation == '-':
                        result[monkey_name] = result[first_monkey] - result[second_monkey]
                    elif operation == '/':
                        result[monkey_name] = result[first_monkey] // result[second_monkey]
                    else:
                        raise Exception('Unknown operation')
            elif isinstance(monkey_yells, int):
                result[monkey_name] = monkey_yells
            else:
                raise Exception('Unknown monkey instruction input')

        if 'root' in result:
            return result['root']


example_input = '''root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32'''.splitlines()

assert solution_for_first_part(example_input) == 152

# The input is taken from: https://adventofcode.com/2022/day/21/input
task_input = list(load_input_file('input.21.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
