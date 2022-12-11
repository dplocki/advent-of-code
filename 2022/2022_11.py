from typing import Generator, Iterable, Tuple
from collections import deque


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def parse(task_input: str) -> Generator[Tuple, None, None]:
    monkeys = task_input.split('\n\n')

    for monkey in monkeys:
        lines = monkey.splitlines()

        id = int(lines[0].split()[1][:-1])
        starting_items = list(map(int, lines[1].split(':')[1].split(',')))
        tokens = lines[2].split()
        operation_value1 = tokens[-3]
        operation = tokens[-2]
        operation_value2 = tokens[-1]
        test_value = int(lines[3].split()[-1])
        in_case_of_true = int(lines[4].split()[-1])
        in_case_of_false = int(lines[5].split()[-1])

        yield (id, starting_items, operation, operation_value1, operation_value2, test_value, in_case_of_true, in_case_of_false)


def solution_for_first_part(task_input: Iterable[str]) -> int:
    monkeys_data = [
        {
            'items': deque(starting_items),
            'operation': eval(f"lambda old: {operation_value1} {operation} {operation_value2}"),
            'test_value': test_value,
            'in_case_of_true': in_case_of_true,
            'in_case_of_false': in_case_of_false,
            'inspects': 0
        }

        for _, starting_items, operation, operation_value1, operation_value2, test_value, in_case_of_true, in_case_of_false in parse(task_input)
    ]

    for _ in range(20):
        for monkey in monkeys_data:
            while monkey['items']:
                monkey['inspects'] += 1

                old = monkey['items'].popleft()
                item = monkey['operation'](old) // 3

                monkeys_data[monkey[
                    'in_case_of_true'
                    if item % monkey['test_value'] == 0
                    else 'in_case_of_false'
                ]]['items'].append(item)

    sorted_monkeys_inspects = sorted(monkey['inspects'] for monkey in monkeys_data)
    return sorted_monkeys_inspects[-1] * sorted_monkeys_inspects[-2]


example_input = '''Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1'''

assert solution_for_first_part(example_input) == 10605

# The input is taken from: https://adventofcode.com/2022/day/11/input
task_input = load_input_file('input.11.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
