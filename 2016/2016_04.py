import re
from functools import reduce 


def load_input_file(file_name):
    pattern = re.compile(r'^([a-z-]+)-([0-9]+)\[([a-z]+)\]$')
    with open(file_name) as file:
        for line in file:
            groups = pattern.match(line.strip())
            yield groups[1], int(groups[2]), groups[3]


def calculate_checksum(room_name):

    def count_letters(result, element):
        if element.isalpha():
            result[element] = result.get(element, 0) + 1
        return result

    return ''.join(
            map(
                lambda x: x[0],
                sorted(
                    reduce(count_letters, room_name, {}).items(),
                    key=lambda s: s[1] * (-1000) + ord(s[0])
                )
            )
        )[:5]


assert calculate_checksum('aaaaa-bbb-z-y-x-123') == 'abxyz'
assert calculate_checksum('a-b-c-d-e-f-g-h-987') == 'abcde'
assert calculate_checksum('not-a-real-room-404') == 'oarel'


def solution_for_first_part(input: [(str, str)]) -> int:
    return sum(
            room_id
            for room_name, room_id, check_sum in input
            if calculate_checksum(room_name) == check_sum
        )


# The input is taken from: https://adventofcode.com/2016/day/4/input
input = load_input_file('input.04.txt')
print("Solution for the first part:", solution_for_first_part(input))
