from typing import Dict, Generator, Iterable, Tuple, Union


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]):
    for line in task_input:
        monkey_name, monkey_instructions = line.split(': ')
        monkey_instructions = monkey_instructions.split(' ')
        yield monkey_name, int(monkey_instructions[0]) if len(monkey_instructions) == 1 else tuple(monkey_instructions)


def find_what_monkey_yells(monkeys_instructions: Dict[str, Union[int, Tuple[str, str, str]]], requested_monkey_name: str) -> int:
    monkey_yells = monkeys_instructions.get(requested_monkey_name, None)

    if isinstance(monkey_yells, int):
        return monkey_yells
    elif isinstance(monkey_yells, tuple):
        first_monkey, operation, second_monkey = monkey_yells

        first_monkey_yells = find_what_monkey_yells(monkeys_instructions, first_monkey)
        second_monkey_yells = find_what_monkey_yells(monkeys_instructions, second_monkey)

        if first_monkey_yells == None or second_monkey_yells == None:
            return None

        if operation == '+':
            return first_monkey_yells + second_monkey_yells
        elif operation == '*':
            return first_monkey_yells * second_monkey_yells
        elif operation == '-':
            return first_monkey_yells - second_monkey_yells
        elif operation == '/':
            return first_monkey_yells // second_monkey_yells
        else:
            raise Exception('Unknown operation')
    else:
        return None


def solution_for_first_part(task_input: Iterable[str]) -> int:
    monkeys_instructions = {monkey_name:monkey_yells for monkey_name, monkey_yells in parse(task_input)}

    return find_what_monkey_yells(monkeys_instructions, 'root')


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


def find_value_for_human(monkeys_instructions: Dict[str, Union[int, Tuple[str, str, str]]], result_value: int, monkey_name: str) -> int:
    if monkey_name == 'humn':
        return result_value

    monkeys_yells = monkeys_instructions[monkey_name]
    first_monkey, operation, second_monkey = monkeys_yells
    
    first_monkey_value = find_what_monkey_yells(monkeys_instructions, first_monkey)
    second_monkey_value = find_what_monkey_yells(monkeys_instructions, second_monkey)

    if first_monkey_value == None:
        if operation == '+':
            result_value -= second_monkey_value
        elif operation == '-':
            result_value += second_monkey_value
        elif operation == '*': 
            result_value //= second_monkey_value
        elif operation == '/':
            result_value *= second_monkey_value

        return find_value_for_human(monkeys_instructions, result_value, first_monkey)
    elif second_monkey_value == None:
        if operation == '+':
            result_value -= first_monkey_value
        elif operation == '-':
            result_value = first_monkey_value - result_value
        elif operation == '*': 
            result_value //= first_monkey_value
        elif operation == '/':
            result_value = first_monkey_value // result_value

        return find_value_for_human(monkeys_instructions, result_value, second_monkey)


def solution_for_second_part(task_input: Iterable[str]) -> int:
    monkeys_instructions = {monkey_name:monkey_yells for monkey_name, monkey_yells in parse(task_input) if monkey_name != 'humn'}

    first_monkey_name, _, second_monkey_name = monkeys_instructions['root']
    first_monkey_value = find_what_monkey_yells(monkeys_instructions, first_monkey_name)
    second_monkey_value = find_what_monkey_yells(monkeys_instructions, second_monkey_name)

    if first_monkey_value == None:
        return find_value_for_human(monkeys_instructions, second_monkey_value, first_monkey_name)
    elif second_monkey_value == None:
        return find_value_for_human(monkeys_instructions, first_monkey_value, second_monkey_name)


assert solution_for_second_part(example_input) == 301

print("Solution for the second part:", solution_for_second_part(task_input))
