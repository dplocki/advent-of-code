from typing import Dict, Generator, Iterable, List, Tuple


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def parse(task_input: str) -> Tuple[Dict[str, Tuple], Tuple[int, int, int, int]]:

    def split_by_equal_character(token: str) -> Tuple[str, str]:
        return token.split('=')


    def parse_instruction(raw_instruction: str) -> Tuple:
        if len(raw_instruction) > 1 and raw_instruction[1] in '<>':
            tokens = raw_instruction[2:].split(':')
            return raw_instruction[1], raw_instruction[0], int(tokens[0]), tokens[1]

        return '=', raw_instruction


    def parse_instructions(raw_instructions: str) -> Generator[Tuple[str, Tuple], None, None]:
        for i in raw_instructions.splitlines():
            tokens = i.split('{')
            name = tokens[0]
            instruction_tokens = tokens[1][:-1].split(',')
            yield tokens[0], tuple(map(parse_instruction, instruction_tokens))


    def parse_part_machines(raw_part_machines) -> Generator[Tuple[List, List], None, None]:
        for raw_part_machine in raw_part_machines.splitlines():
            tokens = raw_part_machine[1:-1].split(',')
            yield {name:int(value) for name, value in map(split_by_equal_character, tokens)}


    raw_instructions, raw_part_machines = task_input.split('\n\n')
    return {name:value for name, value in parse_instructions(raw_instructions)}, list(parse_part_machines(raw_part_machines))


def is_accepted(instructions_collection: Dict, where: str, parameters: Dict[str, int]) -> bool:
    if where == 'A':
        return True

    if where == 'R':
        return False

    instructions = instructions_collection[where]
    for instruction in instructions:
        if instruction[0] == '>':
            if parameters[instruction[1]] > instruction[2]:
                return is_accepted(instructions_collection, instruction[3], parameters)

        elif instruction[0] == '<':
            if parameters[instruction[1]] < instruction[2]:
                return is_accepted(instructions_collection, instruction[3], parameters)

        elif instruction[0] == '=':
            return is_accepted(instructions_collection, instruction[1], parameters)

    raise Exception(f'Incorrect instruction: {instruction}')


def solution_for_first_part(task_input: Iterable[str]) -> int:
    instructions, part_machine_parameters = parse(task_input)

    return sum(
        sum(part_machine_parameter.values())
        for part_machine_parameter in part_machine_parameters
        if is_accepted(instructions, 'in', part_machine_parameter))


example_input = '''px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}'''

assert solution_for_first_part(example_input) == 19114

# The input is taken from: https://adventofcode.com/2023/day/19/input
task_input = load_input_file('input.19.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
