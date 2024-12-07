from typing import Callable, Generator, Iterable, List, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[int, Tuple[int, ...]], None, None]:
    for line in task_input:
        tokens = line.split(':')
        result = int(tokens[0])
        numbers = tuple(map(int, tokens[1].split()))

        yield result, numbers


def is_valid_for_two_operators(result: int, numbers: List[int]) -> bool:
    if len(numbers) == 0:
        return result == 0

    if len(numbers) == 1:
        return result == numbers[0]

    first = numbers[0]
    second = numbers[1]

    if is_valid_for_two_operators(result, [first * second] + numbers[2:]):
        return True

    if is_valid_for_two_operators(result, [first + second] + numbers[2:]):
        return True

    return False


def solution(task_input: Iterable[str], is_valid: Callable[[int, List[int]], bool]) -> int:
    return sum(
        result if is_valid(result, list(numbers)) else 0
        for result, numbers in parse(task_input))


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return solution(task_input, is_valid_for_two_operators)


example_input = '''190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20'''.splitlines()

assert solution_for_first_part(example_input) == 3749

# The input is taken from: https://adventofcode.com/2024/day/7/input
task_input = list(load_input_file('input.07.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def is_valid_for_second_operators(result: int, numbers: List[int]) -> bool:
    if len(numbers) == 0:
        return result == 0

    if len(numbers) == 1:
        return result == numbers[0]

    first = numbers[0]
    second = numbers[1]

    if is_valid_for_second_operators(result, [first * second] + numbers[2:]):
        return True

    if is_valid_for_second_operators(result, [first + second] + numbers[2:]):
        return True

    if is_valid_for_second_operators(result, [int(str(first) + str(second))] + numbers[2:]):
        return True

    return False


def solution_for_second_part(task_input: Iterable[str]) -> int:
    return solution(task_input, is_valid_for_second_operators)


print("Solution for the second part:", solution_for_second_part(task_input))
