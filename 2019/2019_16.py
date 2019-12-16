from itertools import cycle
from functools import reduce


def load_input_file(file_name: str):
    with open(file_name) as file:
        return file.read().strip()


def base_pattern_generator(which_position: int):

    def base(which_position: int):
        base = [0, 1, 0, -1]

        for b in cycle(base):
            yield from [b] * which_position

    generator = base(which_position)
    next(generator)
    return generator


def next_phase(previous_phase: [int], input_length):
    previous_phase = list(previous_phase)
    for i in range(input_length):
        second_pattern = base_pattern_generator(i + 1)
        yield abs(sum([p * s for p, s in zip(previous_phase, second_pattern)])) % 10


def solution_for_first_part(input: str):
    input_length = len(input)
    message = map(int, input)
    for _ in range(100):
        message = next_phase(message, input_length)

    return ''.join(map(str, list(message)[:8]))


assert solution_for_first_part('80871224585914546619083218645595') == '24176176'
assert solution_for_first_part('19617804207202209144916044189917') == '73745418'
assert solution_for_first_part('69317163492948606335995924319873') == '52432133'

# The input is taken from: https://adventofcode.com/2019/day/16/input
raw_input = load_input_file('input.16.txt')
print("Solution for the first part:", solution_for_first_part(raw_input))


def solution_for_second_part(raw_input: str):
    get_answer_from = int(raw_input[:7])
    if get_answer_from + 8 > len(raw_input) * 10_000:
        raise Exception('Unposible to solve: 8 seeked digits are outside the message')

    message = list(map(int, (raw_input * 10_000)[get_answer_from:]))
    for _ in range(100):
        sum_of_message = sum(message)

        for i, p in enumerate(message):
            message[i] = sum_of_message % 10
            sum_of_message -= p

    return ''.join(map(str, message[:8]))


assert solution_for_second_part('03036732577212944063491565474664') == '84462026'
assert solution_for_second_part('02935109699940807407585447034323') == '78725270'
assert solution_for_second_part('03081770884921959731165446850517') == '53553731'

print("Solution for the second part:", solution_for_second_part(raw_input))
