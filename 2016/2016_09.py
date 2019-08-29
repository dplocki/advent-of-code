def load_input_file(file_name):
    with open(file_name) as file:
        return file.read().strip()


class Parser():

    def __init__(self):
        self.state = self.normal
        self.buffor = ''
        self.how_many_letters = 0
        self.how_many_repeat = 0

    def normal(self, char):
        if char == '(':
            self.state = self.marker
            return

        return char

    def marker(self, char):
        if char == ')':
            self.how_many_letters, self.how_many_repeat = map(int, self.buffor.split('x'))
            self.state = self.repeat
            self.buffor = ''
        else:
            self.buffor += char

    def repeat(self, char):
        self.buffor += char
        self.how_many_letters -= 1

        if self.how_many_letters == 0:
            tmp = self.buffor * self.how_many_repeat
            self.buffor = ''
            self.state = self.normal

            return tmp

    def decompression(self, line):
        for char in line:
            result = self.state(char)
            if result != None:
                yield from result


def decompressed_length(line: str):
    return sum([1 for _ in Parser().decompression(line)])


assert decompressed_length('ADVENT') == 6
assert decompressed_length('A(1x5)BC') == 7
assert decompressed_length('(3x3)XYZ') == 9
assert decompressed_length('A(2x2)BCD(2x2)EFG') == 11
assert decompressed_length('(6x1)(1x3)A') == 6
assert decompressed_length('X(8x2)(3x3)ABCY') == 18


def decompressed_length_with_internal(line: str) -> int:
    if line[0] == '(':
        close_bracket_index = line.index(')')
        how_many_letter, how_many_repeat = map(int, line[1:close_bracket_index].split('x'))
        
        result = how_many_repeat * decompressed_length_with_internal(line[close_bracket_index + 1:close_bracket_index + how_many_letter + 1])
        if close_bracket_index + how_many_letter + 1 < len(line):
            result += decompressed_length_with_internal(line[close_bracket_index + how_many_letter + 1:])

        return result

    open_bracket_index = line.find('(')
    if open_bracket_index == -1:
        return len(line)

    return open_bracket_index + decompressed_length_with_internal(line[open_bracket_index:])


assert decompressed_length_with_internal('(3x3)XYZ') == len('XYZXYZXYZ')
assert decompressed_length_with_internal('X(8x2)(3x3)ABCY') == len('XABCABCABCABCABCABCY')
assert decompressed_length_with_internal('(27x12)(20x12)(13x14)(7x10)(1x12)A') == 241920
assert decompressed_length_with_internal('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN') == 445


# The input is taken from: https://adventofcode.com/2016/day/9/input
input_string = load_input_file('input.09.txt')
print("Solution for the first part:", decompressed_length(input_string))
print("Solution for the second part:", decompressed_length_with_internal(input_string))
