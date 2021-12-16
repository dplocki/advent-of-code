from __future__ import annotations
from functools import reduce
from operator import mul


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def parse(task_input: str) -> list[int]:
    translate_table = {
        '0': [0,0,0,0],
        '1': [0,0,0,1],
        '2': [0,0,1,0],
        '3': [0,0,1,1],
        '4': [0,1,0,0],
        '5': [0,1,0,1],
        '6': [0,1,1,0],
        '7': [0,1,1,1],
        '8': [1,0,0,0],
        '9': [1,0,0,1],
        'A': [1,0,1,0],
        'B': [1,0,1,1],
        'C': [1,1,0,0],
        'D': [1,1,0,1],
        'E': [1,1,1,0],
        'F': [1,1,1,1],
    }

    for character in task_input:
        yield from translate_table[character]


def bits_to_int(bits: list[int]) -> int:
    result = 0

    for bit in bits:
        result <<= 1
        result += bit

    return result


class BitsProvider():

    def __init__(self, bits: list[int]) -> BitsProvider:
        self.bits = bits
        self.index = 0
        self.len = len(bits)

    def get_bits(self, how_much: int) -> list[int]:
        sub_collection = self.bits[self.index: self.index + how_much]
        self.index += how_much
        return sub_collection

    def bits_left(self) -> bool:
        return self.index != self.len


class Packet():

    def __init__(self, version: int, type: int, numeric_value: int, children: list[Packet]) -> Packet:
        self.version = version
        self.type = type
        self.numeric_value = numeric_value
        self.children = children


def load_packets_hierarchy(bits: list[int]) -> int:
    packet_version = bits_to_int(bits.get_bits(3))
    packet_type = bits_to_int(bits.get_bits(3))

    if packet_type == 4:
        blocks = []
        while True:
            is_last = bits.get_bits(1)[0]
            blocks.extend(bits.get_bits(4))
            if is_last == 0:
                break

        return Packet(packet_version, packet_type, bits_to_int(blocks), [])

    length_type_id = bits.get_bits(1)[0]
    if length_type_id == 0:
        length = bits_to_int(bits.get_bits(15))
        sub_bits = BitsProvider(bits.get_bits(length))
        children = []
        while sub_bits.bits_left():
            children.append(load_packets_hierarchy(sub_bits))
    else:
        length = bits_to_int(bits.get_bits(11))
        children = []
        for _ in range(length):
            children.append(load_packets_hierarchy(bits))

    return Packet(packet_version, packet_type, 0, children)


def solution_for_first_part(task_input: str) -> int:

    def sum_all_version(packet: Packet) -> int:
        return sum(sum_all_version(child) for child in packet.children) + packet.version


    bits = BitsProvider(list(parse(task_input)))
    packets_hierarchy = load_packets_hierarchy(bits)

    return sum_all_version(packets_hierarchy)


assert solution_for_first_part('8A004A801A8002F478') == 16
assert solution_for_first_part('620080001611562C8802118E34') == 12
assert solution_for_first_part('C0015000016115A2E0802F182340') == 23
assert solution_for_first_part('A0016C880162017C3686B18A3D4780') == 31

# The input is taken from: https://adventofcode.com/2021/day/16/input
task_input = load_input_file('input.16.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: str) -> int:

    def evaluate_expression(packet: Packet) -> int:
        if packet.type == 4:
            return packet.numeric_value

        child_values = [evaluate_expression(child) for child in packet.children]

        if packet.type == 0:
            return sum(child_values)

        elif packet.type == 1:
            return reduce(mul, child_values)

        elif packet.type == 2:
            return min(child_values)

        elif packet.type == 3:
            return max(child_values)

        elif packet.type == 5:
            assert len(child_values) == 2
            return 1 if child_values[0] > child_values[1] else 0

        elif packet.type == 6:
            assert len(child_values) == 2
            return 1 if child_values[0] < child_values[1] else 0

        elif packet.type == 7:
            assert len(child_values) == 2
            return 1 if child_values[0] == child_values[1] else 0

        raise Exception('unknown type')


    bits = BitsProvider(list(parse(task_input)))
    packets_hierarchy = load_packets_hierarchy(bits)

    return evaluate_expression(packets_hierarchy)


assert solution_for_second_part('C200B40A82') == 3
assert solution_for_second_part('04005AC33890') == 54
assert solution_for_second_part('880086C3E88112') == 7
assert solution_for_second_part('CE00C43D881120') == 9
assert solution_for_second_part('D8005AC2A8F0') == 1
assert solution_for_second_part('F600BC2D8F') == 0
assert solution_for_second_part('9C005AC2F8F0') == 0
assert solution_for_second_part('9C0141080250320F1802104A08') == 1

print("Solution for the second part:", solution_for_second_part(task_input))