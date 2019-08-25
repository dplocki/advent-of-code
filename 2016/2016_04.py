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


def solution_for_first_part(input: [(str, int, str)]) -> int:
    return sum(
            room_id
            for room_name, room_id, check_sum in input
            if calculate_checksum(room_name) == check_sum
        )


def decrypt_room_name(room_name: str, room_id: int) -> str:
    ord_a = ord('a')

    return ''.join(
            map(
                lambda x: chr(ord_a + ((ord(x) - ord_a) + room_id) % 26) if x.isalpha() else ' ',
                room_name
            )
        )


assert decrypt_room_name('qzmt-zixmtkozy-ivhz', 343) == 'very encrypted name'


def solution_for_second_part(input: [(str, int, str)]):
    for room_name, room_id, check_sum in input:
        if calculate_checksum(room_name) == check_sum:
            real_name = decrypt_room_name(room_name, room_id)
            if 'northpole' in real_name:
                return room_id


# The input is taken from: https://adventofcode.com/2016/day/4/input
input = list(load_input_file('input.04.txt'))
print("Solution for the first part:", solution_for_first_part(input))
print("Solution for the second part:", solution_for_second_part(input))
