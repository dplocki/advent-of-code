from functools import reduce


def load_input_file(file_name: str) -> [str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def solution_for_first_part(task_input: [str]) -> int:

    def parse(lines: [str]) -> [set]:
        result = set()

        for line in lines:
            if line == '':
                yield result
                result = set()
            else:
                result.update((c for c in line))

        yield result


    return sum(len(r) for r in parse(task_input))
        

assert solution_for_first_part('''abc

a
b
c

ab
ac

a
a
a
a

b'''.splitlines()) == 11

# The input is taken from: https://adventofcode.com/2020/day/6/input
task_input = list(load_input_file('input.06.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: [str]) -> int:

    def parse(lines: [str]) -> [[set]]:
        result = []

        for line in lines:
            if line == '':
                yield result
                result = []
            else:
                result.append(set(line))

        yield result

    def common_part(a: set, b: set) -> set:
        return a & b


    return sum(
            len(reduce(common_part, group_responses))
            for group_responses in parse(task_input)
        )


assert solution_for_second_part('''abc
abc

a
b
c

ab
ac

a
a
a
a

b'''.splitlines()) == 6

print("Solution for the second part:", solution_for_second_part(task_input))
