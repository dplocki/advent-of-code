from typing import Callable, Dict, Generator, Iterable, List, Tuple
import re


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read()


def parse_line(instruction_lines: Iterable[str]) -> Generator[Tuple[int, int, int], None, None]:
    pattern = re.compile(r'move (\d+) from (\d+) to (\d+)')
    for line in instruction_lines:
        groups = pattern.match(line)
        yield int(groups[1]), int(groups[2]), int(groups[3])


def parse(task_input: List[str]) -> Tuple[Dict[int, List[str]]]:
    stacks_description, instructions = task_input.split('\n\n')
    stacks_description = stacks_description.split('\n')[:-1]

    stacks = {}

    for line in stacks_description:
        for index, character in enumerate(line):
            if character not in '[] \n':
                stack_index = ((index - 1) // 4) + 1
                stack = stacks.get(stack_index, [])
                stack.append(character)
                stacks[stack_index] = stack


    return stacks, instructions.splitlines()


def solution(task_input: str, run_crane: Callable[[Dict[int, List[str]], int, int, int], None]) -> str:
    stacks, instructions = parse(task_input)
    stacks = {k:list(reversed(v)) for k, v in stacks.items()}

    for how_many, _from, _to in parse_line(instructions):
        run_crane(stacks, how_many, _from, _to)

    return ''.join(stacks[index].pop() for index in sorted(stacks.keys()))


def solution_for_first_part(task_input: str) -> str:

    def internal(stacks, how_many, start, end):
        for _ in range(how_many):
            container = stacks[start].pop()
            stacks[end].append(container)

    return solution(task_input, internal)


example_input = '''    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2'''

assert solution_for_first_part(example_input) == 'CMZ'

# The input is taken from: https://adventofcode.com/2022/day/5/input
task_input = load_input_file('input.05.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: str) -> str:

    def internal(stacks, how_many, start, end):
        to_moved = [stacks[start].pop() for _ in range(how_many)]
        to_moved.reverse()

        for container in to_moved:
            stacks[end].append(container)

    return solution(task_input, internal)


assert solution_for_second_part(example_input) == 'MCD'
print("Solution for the second part:", solution_for_second_part(task_input))
