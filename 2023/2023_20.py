from collections import deque
from itertools import count
from typing import Generator, Iterable, List, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[str, Tuple[str, ...]], None, None]:
    for line in task_input:
        tokens = line.split(' -> ')
        output = tuple(tokens[1].split(', '))

        if tokens[0][0] in '%&':
            yield tokens[0][0], tokens[0][1:], output
        else:
            yield None, tokens[0], output


def run(task_input: Iterable[str]) -> Generator[Tuple, None, None]:
    flip_flops = {}
    conjunctions = {}
    modules = {}

    for type, name, output in parse(task_input):
        modules[name] = output

        if type == '%':
            flip_flops[name] = False
        elif type == '&':
            conjunctions[name] = {}

    for conjunction in conjunctions.keys():
        for name, output in modules.items():
            if conjunction in output:
                conjunctions[conjunction][name] = False

    for pressed_button_count in count(1):
        yield 'button pressed', pressed_button_count, None

        events = deque([('broadcaster', False, 'button')])

        while events:
            where, impulse, source = events.popleft()
            yield 'event', where, impulse

            if where == 'broadcaster':
                events.extend((output, impulse, where) for output in modules[where])

            elif where in flip_flops:
                if not impulse:
                    events.extend((output, not flip_flops[where], where) for output in modules[where])
                    flip_flops[where] = not flip_flops[where]

            elif where in conjunctions:
                conjunctions[where][source] = impulse
                impulse_to_send = all(conjunctions[where].values())
                events.extend((output, not impulse_to_send, where) for output in modules[where])


def solution_for_first_part(task_input: List[str]) -> int:
    high_impulse_count, low_impulse_count = 0, 0
    pressed_button_count = 0

    for event_type, where, impulse in run(task_input):
        if event_type == 'button pressed':
            pressed_button_count = where
            if pressed_button_count > 1000:
                break

            continue

        elif event_type == 'event':

            if impulse:
                high_impulse_count += 1
            else:
                low_impulse_count += 1

    return high_impulse_count * low_impulse_count


example_input = '''broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
'''.splitlines()

example_input_2 = '''broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output'''.splitlines()

assert solution_for_first_part(example_input) == 32000000
assert solution_for_first_part(example_input_2) == 11687500

# The input is taken from: https://adventofcode.com/2023/day/20/input
task_input = list(load_input_file('input.20.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
