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

    def __init__(self, bits: list[int]) -> None:
        self.bits = bits
        self.index = 0
        self.len = len(bits)

    def get_bits(self, how_much: int) -> list[int]:
        sub_collection = self.bits[self.index: self.index + how_much]
        self.index += how_much
        return sub_collection

    def bits_left(self) -> bool:
        return self.index != self.len


def read_packets_version(bits: list[int]) -> int:
    packet_version = bits_to_int(bits.get_bits(3))
    packet_type = bits_to_int(bits.get_bits(3))

    if packet_type == 4:
        while True:
            block = bits.get_bits(5)
            if block[0] == 0:
                return packet_version
    else:
        length_type_id = bits.get_bits(1)[0]
        if length_type_id == 0:
            length = bits_to_int(bits.get_bits(15))

            other_bits = BitsProvider(bits.get_bits(length))
            result = packet_version
            while other_bits.bits_left():
                block_result = read_packets_version(other_bits)
                result += block_result

            return result
        else:
            lenght = bits_to_int(bits.get_bits(11))
            result = packet_version
            for _ in range(lenght):
                result += read_packets_version(bits)

            return result


def solution_for_first_part(task_input: str) -> int:
    bits = BitsProvider(list(parse(task_input)))
    result = read_packets_version(bits)
    return result


assert solution_for_first_part('8A004A801A8002F478') == 16
assert solution_for_first_part('620080001611562C8802118E34') == 12
assert solution_for_first_part('C0015000016115A2E0802F182340') == 23
assert solution_for_first_part('A0016C880162017C3686B18A3D4780') == 31

# The input is taken from: https://adventofcode.com/2021/day/16/input
task_input = load_input_file('input.16.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
