from functools import reduce 
from operator import mul, itemgetter


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def solution_for_first_part(task_input: [str]) -> int:

    def parse(task_input: [str]):
        timestamp, buses = task_input.splitlines()
        return int(timestamp), (int(x) for x in buses.split(',') if x != 'x')


    timestamp, buses = parse(task_input)
    earliest_bus = min(((bus, ((timestamp // bus + 1) * bus) - timestamp) for bus in buses), key=itemgetter(1))

    return reduce(mul, earliest_bus)


example_input = '''939
7,13,x,x,59,x,31,19'''

assert solution_for_first_part(example_input) == 295

# The input is taken from: https://adventofcode.com/2020/day/13/input
task_input = load_input_file('input.13.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: [str]) -> int:

    def parse(task_input: [str]) -> tuple:
        return (
            int(x) if x != 'x' else None
            for x in task_input.splitlines()[1].split(','))
 
    def modular_inverse(a: int, b: int) -> int:
        if b == 1:
            return 1

        b0 = b
        x0, x1 = 0, 1
        while a > 1:
            q = a // b
            a, b = b, a % b
            x0, x1 = x1 - q * x0, x0

        if x1 < 0:
            x1 += b0

        return x1
 

    def solve_chinese_remainder_theorem(congruences: list) -> int:
        product = reduce(mul, map(itemgetter(1), congruences))

        solution = 0
        for a_i, n_i in congruences:
            p = product // n_i
            solution += a_i * modular_inverse(p, n_i) * p

        return solution % product


    return solve_chinese_remainder_theorem([
            (-i, bus)
            for i, bus in enumerate(parse(task_input))
            if bus != None
        ])


assert solution_for_second_part(example_input) == 1068781
assert solution_for_second_part('\n17,x,13,19') == 3417
assert solution_for_second_part('\n67,7,59,61') == 754018
assert solution_for_second_part('\n67,x,7,59,61') == 779210
assert solution_for_second_part('\n67,7,x,59,61') == 1261476
assert solution_for_second_part('\n1789,37,47,1889') == 1202161486

print("Solution for the first part:", solution_for_second_part(task_input))
